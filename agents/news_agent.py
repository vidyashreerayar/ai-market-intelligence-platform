import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from database.query import get_latest_news

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

# Bind the tool to the model
llm_with_tools = llm.bind_tools([get_latest_news])


def answer_question(question: str):

    response = llm_with_tools.invoke(
        [HumanMessage(content=question)]
    )

    if response.tool_calls:

        tool_call = response.tool_calls[0]

        if tool_call["name"] == "get_latest_news":
            tool_result = get_latest_news.invoke(tool_call["args"])

            final_response = llm.invoke(
                f"""
You are an AI assistant for Intersnack.

Here is the retrieved news:

{tool_result}

Answer the user's question.

Question:
{question}
"""
            )

            return {
                "text": final_response.content,
                "chart_data": None,
                "chart_title": None,
                "chart_type": None
            }

    return {
        "text": response.content,
        "chart_data": None,
        "chart_title": None,
        "chart_type": None
    }


if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer["text"])