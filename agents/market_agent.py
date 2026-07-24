import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from database.query import get_latest_news

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


def answer_question(question: str):

    articles = get_latest_news.invoke({"limit": 10})

    prompt = f"""
You are the Market Intelligence Agent for Intersnack.

Below are the latest news articles:

{articles}

Your responsibilities are:
- Identify competitor activities.
- Identify new product launches.
- Identify market opportunities.
- Highlight risks to Intersnack.

If the information is unavailable, state that clearly.
Do not make up facts.

User question:
{question}
"""

    response = llm.invoke(prompt)

    return {
        "text": response.content,
        "chart_data": None,
        "chart_title": None,
        "chart_type": None
    }


if __name__ == "__main__":
    while True:
        question = input("\nAsk Market Agent (or type 'exit'): ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer["text"])