from etl.extract import PricingExtractor
from etl.transform import PricingTransformer, NewsTransformer
from etl.load import DatabaseLoader
from etl.indexer import NewsIndexer
from scrapers.news_api import NewsAPIExtractor

# Define news search topics grouped by the type of information needed
NEWS_QUERIES = {
    "general_news": ["snacks", "Intersnack", "potato chips"],
    "competitor_retail": ["Lays", "Pringles", "Doritos", "PepsiCo snacks", "Mondelez snacks"],
    "consumer_trend": ["healthy snacking trend", "snack industry growth"],
}


def run_pipeline():                                                      # Run the complete data extraction, transformation, loading, and indexing process

    loader = DatabaseLoader()                                            # Create an object to load data into PostgreSQL
    indexer = NewsIndexer()                                              # Create an object to index news for later retrieval
    indexer.ensure_schema()                                              # Make sure the required database/index structure exists

    # ---------- News ----------
    # Create objects to fetch news and clean the extracted news data
    news_extractor = NewsAPIExtractor()
    news_transformer = NewsTransformer()

    for category, queries in NEWS_QUERIES.items():                      # Go through each news category and its list of search queries
        for query in queries:                                           # Process each search query one at a time
            news_df = news_extractor.fetch_news(query=query)            # Fetch news articles for the current search query
            news_df = news_transformer.clean(news_df)                   # Clean the fetched news data

            inserted = loader.load_dataframe(news_df, "news_articles")   # Load the cleaned news data into the news_articles table
            print(f"News ({query}): {inserted} rows loaded.")             # Show how many rows were loaded for this query

        
            indexed = indexer.index_dataframe(news_df, category=category)   # Index the cleaned news (create embeddings for later AI retrieval)
            print(f"News ({query}): {indexed} rows indexed.")               # Show how many news articles were indexed for the current query

    # ---------- Pricing ----------
    pricing_extractor = PricingExtractor()                                  # Create an object to get pricing data from Eurostat
    pricing_transformer = PricingTransformer()                              # Create an object to transform the raw pricing data

    raw_data = pricing_extractor.extract()                                  # Get the raw JSON data from Eurostat
    pricing_df = pricing_transformer.transform(raw_data)                    # Convert the raw Eurostat data into a structured DataFrame

    inserted = loader.load_dataframe(pricing_df, "potato_prices")           # Load the pricing DataFrame into the potato_prices database table
    print(f"Pricing: {inserted} rows loaded.")                              # Show how many pricing rows were loaded
    # Note: pricing data stays structured (no embedding needed) — the pricing_agent
    # queries potato_prices directly rather than via RAG retrieval.


if __name__ == "__main__":
    run_pipeline()