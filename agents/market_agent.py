# Load environment variables and required libraries
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from etl.indexer import NewsIndexer

load_dotenv()
# Set up the LLM used to analyze competitor and market news
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)
# Create a NewsIndexer object from the NewsIndexer class defined in etl/indexer.py
_indexer = NewsIndexer()

# Retrieve relevant competitor news and generate a market analysis
def answer_question(question: str):

    # Retrieve the 8 most relevant articles from the competitor_retail category
    retrieved = _indexer.retrieve(query=question, top_k=8, category="competitor_retail")
    # Return a message if no relevant competitor or market articles were found
    if not retrieved:
        return {
            "text": "I don't have any indexed competitor/market news relevant to that question yet.",
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
    # Define instructions for the LLM to analyze competitor and market information
    prompt = f"""
You are the Market Intelligence Agent for Intersnack.

Below are the most relevant retrieved news articles:

{context_block}

Your responsibilities are:
- Identify competitor activities.
- Identify new product launches.
- Identify market opportunities.
- Highlight risks to Intersnack.

Cite the source number for every factual claim, e.g. [Source 1].
If the information is unavailable in the sources above, state that clearly.
Do not make up facts.

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
    # Return the market analysis and its supporting sources
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
        question = input("\nAsk Market Agent (or type 'exit'): ")

        if question.lower() == "exit":
            break
        # Display the supporting sources if any were returned
        answer = answer_question(question)

        print("\nAnswer:")
        print(answer["text"])
        if answer.get("sources"):
            print("\nSources:")
            for s in answer["sources"]:
                print(f"  [{s['label']}] {s['title']} — {s['url']} (similarity: {s['similarity']})")