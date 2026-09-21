#SentenceTransformer is used to convert news text into embeddings, 
# while SQLAlchemy and the database engine are used for PostgreSQL operations.
#The local all-MiniLM-L6-v2 model produces 384-dimensional embeddings.
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from database.connection import engine

EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 384-dim, local, free
EMBEDDING_DIM = 384

class NewsIndexer:
    """
    Embeds news articles into a pgvector table for RAG retrieval.
    Runs after DatabaseLoader.load_dataframe() so it only embeds newly inserted rows.
    """
    #The class handles converting news articles into embeddings and storing them for semantic retrieval.
    #The PostgreSQL engine and embedding model are initialized when the indexer is created.
    def __init__(self):
        self.engine = engine
        self.model = SentenceTransformer(EMBEDDING_MODEL)
    
    #The pgvector extension and news_embeddings table are created if they do not already exist.
    #A vector index is also created to make similarity-based retrieval more efficient.
    def ensure_schema(self):
        with self.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS news_embeddings (
                    id SERIAL PRIMARY KEY,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    source TEXT,
                    published_at TIMESTAMP,
                    category TEXT,
                    embedding VECTOR({EMBEDDING_DIM})
                );
            """))
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_news_embedding
                    ON news_embeddings USING ivfflat (embedding vector_cosine_ops);
            """))
            conn.commit()
    #Incoming news articles are checked against URLs already present in news_embeddings, so only unindexed articles are processed.
    #Each new article is converted into an embedding and stored in PostgreSQL together with its metadata and category.
    def index_dataframe(self, df, category: str = "general_news"):
        """Embed and store rows not already indexed (by url)."""
        if df.empty:
            return 0

        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT url FROM news_embeddings"))
            already_indexed = {row[0] for row in result}

        new_rows = df[~df["url"].isin(already_indexed)]
        if new_rows.empty:
            print("No new articles to index.")
            return 0

        with self.engine.connect() as conn:
            for _, row in new_rows.iterrows():
                content = f"{row['title']}\n\n{row.get('description') or ''}".strip()
                if len(content) < 20:
                    continue  #Skips articles with almost no useful text.

                embedding = self.model.encode(content).tolist()

                conn.execute(
                    text("""
                        INSERT INTO news_embeddings
                            (url, title, description, source, published_at, category, embedding)
                        VALUES (:url, :title, :description, :source, :published_at, :category, :embedding)
                        ON CONFLICT (url) DO NOTHING
                    """),
                    {
                        "url": row["url"],
                        "title": row["title"],
                        "description": row.get("description"),
                        "source": row.get("source"),
                        "published_at": row.get("published_at"),
                        "category": category,
                        "embedding": embedding,
                    },
                )
            conn.commit()

        print(f"Indexed {len(new_rows)} new articles into news_embeddings.")
        return len(new_rows)
    #The user's query is converted into an embedding using the same model.
    #PostgreSQL then finds the most semantically similar news articles using vector similarity and returns the top results.
    def retrieve(self, query: str, top_k: int = 5, category: str = None):
        query_embedding = self.model.encode(query).tolist()

        category_filter = "WHERE category = :category" if category else ""
        params = {"embedding": str(query_embedding), "top_k": top_k}
        if category:
            params["category"] = category

        with self.engine.connect() as conn:
            result = conn.execute(
                text(f"""
                    SELECT title, description, url, source, published_at,
                           1 - (embedding <=> :embedding) AS similarity
                    FROM news_embeddings
                    {category_filter}
                    ORDER BY embedding <=> :embedding
                    LIMIT :top_k
                """),
                params,
            )
            rows = result.fetchall()

        return [
            {
                "title": r[0], "description": r[1], "url": r[2],
                "source": r[3], "published_at": r[4], "similarity": r[5],
            }
            for r in rows
        ]