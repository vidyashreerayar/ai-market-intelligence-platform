# Load environment variables and required libraries
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from etl.indexer import NewsIndexer

load_dotenv()
# Set up the LLM used to analyze consumer trends from retrieved news
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)
# Create a NewsIndexer object from the NewsIndexer class defined in etl/indexer.py
_indexer = NewsIndexer()

# Retrieve relevant consumer-trend news and generate an analysis
def answer_question(question: str):

    # Retrieve the 10 most relevant articles from the consumer_trend category
    retrieved = _indexer.retrieve(query=question, top_k=10, category="consumer_trend")
    # Return a message if no relevant trend articles were found
    if not retrieved:
        return {
            "text": "I don't have any indexed trend-related news relevant to that question yet.",
            "chart_data": None,
            "chart_title": None,
            "chart_type": None,
            "sources": []
        }
    # Format the retrieved articles into one text block for the LLM
    context_block = "\n\n".join(
        f"[Source {i+1}: {r['source']}, published {r['published_at']}]\n"
        f"{r['title']}\n{r['description'] or ''}"
        for i, r in enumerate(retrieved)
    )
    # Define instructions for the LLM to analyze the retrieved consumer-trend news
    prompt = f"""
You are the Trend Analysis Agent for Intersnack.

Below are the most relevant retrieved news articles:

{context_block}

Your responsibilities are:
- Identify recurring themes.
- Identify emerging consumer trends.
- Highlight changes in the snack and food industry.
- Mention whether each trend is increasing or decreasing if the articles suggest it.
- Explain why these trends matter to Intersnack.

Cite the source number for every factual claim, e.g. [Source 1].
Do not invent facts.
Use only the provided news articles.

User question:
{question}
"""
    # Send the retrieved articles and analysis instructions to the LLM
    response = llm.invoke(prompt)
    # Prepare the supporting article details for display to the user
    sources = [
        {"label": f"Source {i+1}", "title": r["title"], "url": r["url"],
         "source": r["source"], "similarity": round(r["similarity"], 3)}
        for i, r in enumerate(retrieved)
    ]
    # Return the trend analysis and its supporting sources
    return {
        "text": response.content,
        "chart_data": None,
        "chart_title": None,
        "chart_type": None,
        "sources": sources
    }

# Run a simple terminal interface when this file is run directly
if __name__ == "__main__":
    while True:
        question = input("\nAsk Trend Agent (or type 'exit'): ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer["text"])
        if answer.get("sources"):
            print("\nSources:")
            for s in answer["sources"]:
                print(f"  [{s['label']}] {s['title']} — {s['url']} (similarity: {s['similarity']})")