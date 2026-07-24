import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from database.query import get_potato_prices, get_potato_prices_data

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

llm_with_tools = llm.bind_tools([get_potato_prices])


def answer_question(question: str):

    response = llm_with_tools.invoke(
        [HumanMessage(content=question)]
    )

    if response.tool_calls:

        tool_call = response.tool_calls[0]

        if tool_call["name"] == "get_potato_prices":
            tool_result = get_potato_prices.invoke({})

            final_response = llm.invoke(
                f"""
You are an AI pricing analyst for Intersnack.

You analyze potato price data and provide business insights.

Here is the historical potato price data:

{tool_result}

Answer the user's question using the data above.
If appropriate, mention trends, price increases/decreases, and potential impact on snack manufacturing costs.

Question:
{question}
"""
            )

            return {
                "text": final_response.content,
                "chart_data": get_potato_prices_data(),
                "chart_title": "Potato Prices Over Time (€ per 100kg)",
                "chart_type": "line"
            }

    return {
        "text": response.content,
        "chart_data": None,
        "chart_title": None,
        "chart_type": None
    }


if __name__ == "__main__":
    while True:
        question = input("\nAsk a pricing question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer["text"])