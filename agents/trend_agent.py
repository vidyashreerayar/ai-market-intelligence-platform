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

    articles = get_latest_news.invoke({"limit": 15})

    prompt = f"""
You are the Trend Analysis Agent for Intersnack.

Below are the latest news articles:

{articles}

Your responsibilities are:
- Identify recurring themes.
- Identify emerging consumer trends.
- Highlight changes in the snack and food industry.
- Mention whether each trend is increasing or decreasing if the articles suggest it.
- Explain why these trends matter to Intersnack.

Do not invent facts.
Use only the provided news articles.

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
        question = input("\nAsk Trend Agent (or type 'exit'): ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer["text"])