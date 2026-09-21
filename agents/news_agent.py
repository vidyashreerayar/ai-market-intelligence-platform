# Load environment variables and required libraries
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from etl.indexer import NewsIndexer

load_dotenv()

# Set up the LLM used to generate answers from retrieved news
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

# Create a NewsIndexer object from the NewsIndexer class defined in etl/indexer.py
_indexer = NewsIndexer()

# Retrieve relevant news articles from the indexed news stored in PostgreSQL and use the LLM to answer the user's question
def answer_question(question: str, category: str = None):
    # Find the most relevant indexed news articles for the question
    retrieved = _indexer.retrieve(query=question, top_k=5, category=category)
    # Return a message if no relevant articles were found
    if not retrieved:
        return {
            "text": "I don't have any indexed news relevant to that question yet.",
            "chart_data": None,
            "chart_title": None,
            "chart_type": None,
            "sources": []
        }
    # Combine the retrieved articles into a source block for the LLM
    context_block = "\n\n".join(
        f"[Source {i+1}: {r['source']}, published {r['published_at']}]\n"
        f"{r['title']}\n{r['description'] or ''}"
        for i, r in enumerate(retrieved)
    )
    # Ask the LLM to answer using only the retrieved sources
    final_response = llm.invoke(
        f"""
You are an AI assistant for Intersnack.

Answer the question using ONLY the numbered sources below.
Cite the source number for every factual claim, e.g. [Source 1].
If the sources don't fully answer the question, say so rather than guessing.

Sources:
{context_block}

Question:
{question}
"""
    )
    # Prepare source details so the application can show where the answer came from
    sources = [
        {"label": f"Source {i+1}", "title": r["title"], "url": r["url"],
         "source": r["source"], "similarity": round(r["similarity"], 3)}
        for i, r in enumerate(retrieved)
    ]
     # Return the answer and its supporting sources
    return {
        "text": final_response.content,
        "chart_data": None,
        "chart_title": None,
        "chart_type": None,
        "sources": sources
    }

# test run: Run a simple terminal interface when this file is run directly
if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer["text"])
        if answer.get("sources"):
            print("\nSources:")
            for s in answer["sources"]:
                print(f"  [{s['label']}] {s['title']} — {s['url']} (similarity: {s['similarity']})")