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


def answer_question(question: str, category: str = None):

    retrieved = _indexer.retrieve(query=question, top_k=5, category=category)

    if not retrieved:
        return {
            "text": "I don't have any indexed news relevant to that question yet.",
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

    sources = [
        {"label": f"Source {i+1}", "title": r["title"], "url": r["url"],
         "source": r["source"], "similarity": round(r["similarity"], 3)}
        for i, r in enumerate(retrieved)
    ]

    return {
        "text": final_response.content,
        "chart_data": None,
        "chart_title": None,
        "chart_type": None,
        "sources": sources
    }


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