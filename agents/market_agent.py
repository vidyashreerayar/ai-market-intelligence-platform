import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from etl.indexer import NewsIndexer

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

_indexer = NewsIndexer()


def answer_question(question: str):

    # Retrieve relevant, cited articles from the competitor_retail category
    # (populated by etl/pipeline.py) instead of pulling the latest 10 unfiltered
    retrieved = _indexer.retrieve(query=question, top_k=8, category="competitor_retail")

    if not retrieved:
        return {
            "text": "I don't have any indexed competitor/market news relevant to that question yet.",
            "chart_data": None,
            "chart_title": None,
            "chart_type": None,
            "sources": []
        }

    context_block = "\n\n".join(
        f"[Source {i+1}: {r['source']}, published {r['published_at']}]\n"
        f"{r['title']}\n{r['description'] or ''}"
        for i, r in enumerate(retrieved)
    )

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

    response = llm.invoke(prompt)

    sources = [
        {"label": f"Source {i+1}", "title": r["title"], "url": r["url"],
         "source": r["source"], "similarity": round(r["similarity"], 3)}
        for i, r in enumerate(retrieved)
    ]

    return {
        "text": response.content,
        "chart_data": None,
        "chart_title": None,
        "chart_type": None,
        "sources": sources
    }


if __name__ == "__main__":
    while True:
        question = input("\nAsk Market Agent (or type 'exit'): ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer["text"])
        if answer.get("sources"):
            print("\nSources:")
            for s in answer["sources"]:
                print(f"  [{s['label']}] {s['title']} — {s['url']} (similarity: {s['similarity']})")