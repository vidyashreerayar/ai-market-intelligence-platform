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

    # Retrieve relevant, cited articles from the consumer_trend category
    # (populated by etl/pipeline.py) instead of pulling the latest 15 unfiltered
    retrieved = _indexer.retrieve(query=question, top_k=10, category="consumer_trend")

    if not retrieved:
        return {
            "text": "I don't have any indexed trend-related news relevant to that question yet.",
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