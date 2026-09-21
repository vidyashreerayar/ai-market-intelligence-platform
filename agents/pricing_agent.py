# Load environment variables and required libraries
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from database.query import get_potato_prices, get_potato_prices_data

load_dotenv()
# Set up the LLM used to understand pricing questions and analyze the retrieved data
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)
# Give the LLM access to the potato-price retrieval tool from database/query.py
llm_with_tools = llm.bind_tools([get_potato_prices])

# Handle potato-price questions and return the analysis with chart data
def answer_question(question: str):
    # Send the user's question to the LLM so it can decide whether potato-price data is needed
    response = llm_with_tools.invoke(
        [HumanMessage(content=question)]
    )
    # Check whether the LLM requested the potato-price retrieval tool
    if response.tool_calls:
        # Get the tool call requested by the LLM
        tool_call = response.tool_calls[0]
        # Check that the requested tool is the potato-price retrieval function
        if tool_call["name"] == "get_potato_prices":
            # Run the tool to retrieve the stored potato-price data
            tool_result = get_potato_prices.invoke({})
            # Give the retrieved data to the LLM to generate the business analysis
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
            # Return the written analysis together with the historical price data for the chart
            return {
                "text": final_response.content,
                "chart_data": get_potato_prices_data(),
                "chart_title": "Potato Prices Over Time (€ per 100kg)",
                "chart_type": "line"
            }
    # Return the LLM's response if the potato-price tool was not requested
    return {
        "text": response.content,
        "chart_data": None,
        "chart_title": None,
        "chart_type": None
    }

# Run a simple terminal interface when this file is run directly
if __name__ == "__main__":
    while True:
        question = input("\nAsk a pricing question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer["text"])