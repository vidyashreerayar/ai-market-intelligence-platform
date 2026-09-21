# Import tools for LLM routing, agent execution, logging, and performance tracking
import os
import json
import time
import logging
from groq import Groq

from agents.news_agent import answer_question as news_agent
from agents.market_agent import answer_question as market_agent
from agents.trend_agent import answer_question as trend_agent
from agents.pricing_agent import answer_question as pricing_agent
from etl.metrics import log_query_metrics, log_prompt

# Create a logger to record events and warnings from this file
logger = logging.getLogger(__name__)

# Lookup table to map each intent category to the agent that handles it
AGENT_MAP = {
    "commodity_price": pricing_agent,
    "competitor_retail": market_agent,
    "consumer_trend": trend_agent,
    "general_news": news_agent,
}

# Define the meaning of each category so the LLM can classify questions correctly
INTENT_DESCRIPTIONS = {
    "commodity_price": "Raw material prices, commodity trends, potato/oil costs, inflation, currency (EUR), '100kg' pricing",
    "competitor_retail": "Competitors, brands, market share, product launches (Lays, Pringles, Doritos, PepsiCo, Kellogg, Mondelez)",
    "consumer_trend": "Consumer preferences, trending topics, growth, industry demand, future outlook, behavior",
    "general_news": "Anything else — general news, or queries that don't clearly fit the other categories",
}

# Set the minimum confidence required to trust the classification
CONFIDENCE_THRESHOLD = 0.6

# Define the instructions used by the LLM to classify each user question
# Convert the INTENT_DESCRIPTIONS(above) dictionary into formatted JSON text
# and insert the category definitions into the system prompt for the LLM
# Require the LLM to return only the category and confidence in JSON format
SYSTEM_PROMPT = f"""You are an intent classifier for a snack industry business intelligence assistant.
Classify the user's question into ONE of these categories:

{json.dumps(INTENT_DESCRIPTIONS, indent=2)}

Return ONLY valid JSON in this exact format:
{{"category": "<category_name>", "confidence": <0.0-1.0>}}

Be honest about confidence — if the question is ambiguous or doesn't clearly match a category, use a low confidence score rather than guessing.
"""

_groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Standardize the output from different agents into one consistent format
def _normalize_response(result):                                               # if agent returns dict format result, it is retained and later used in the same format
    if isinstance(result, dict):
        return {
            "text": result.get("text", ""),
            "chart_data": result.get("chart_data"),
            "chart_title": result.get("chart_title"),
            "chart_type": result.get("chart_type"),
            "sources": result.get("sources", [])
        }

    return {                                                                   # if agent returns output as plain text, its converted to the dictionary structure.
        "text": result,
        "chart_data": None,
        "chart_title": None,
        "chart_type": None,
        "sources": []
    }

# note: If classification fails, the error is logged, but the user is shown a general_news answer
# without being informed that the specific information requested was not found or that a fallback was used.
def classify_intent(question: str) -> dict:                                    # method to classify the user's question and return the category with its confidence score
    """Returns {'category': str, 'confidence': float}. Falls back to general_news on any error."""
    try:                                                                       # Try to classify the question using the LLM 
        completion = _groq_client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=0.0,
            response_format={"type": "json_object"},
        )
        result = json.loads(completion.choices[0].message.content)
        if result.get("category") not in INTENT_DESCRIPTIONS:
            raise ValueError(f"Unknown category returned: {result.get('category')}")
        return result
    except Exception as e:                                                      # Log the classification error without stopping the application
        logger.warning(f"Intent classification failed ({e}), falling back to general_news")
        return {"category": "general_news", "confidence": 0.0}                  # Use general_news as the safe fallback when classification fails


def route_question(question: str):           # Classify the question and route it to the appropriate agent                                   
    start_time = time.monotonic()            # Start a timer to measure how long the question takes to process                                   

    result = classify_intent(question)       # Use the LLM to classify the question and return both category and confidence
    category = result["category"]            # Extract only the category value from the result and store in a variable
    confidence = result["confidence"]        # Extract only the confidence score value from the same result and store in a variable

    if confidence < CONFIDENCE_THRESHOLD:
        logger.info(f"Low confidence ({confidence:.2f}) for '{question}' — using general_news fallback")
        category = "general_news"

    agent_fn = AGENT_MAP.get(category, news_agent)
    logger.info(f"Routed to '{category}' (confidence {confidence:.2f}): {agent_fn.__module__}")

    # Log the question, category, and system prompt used for this query
    try:
        log_prompt(question=question, category=category, system_prompt=SYSTEM_PROMPT)
    # If prompt logging fails, record the error without stopping the main process    
    except Exception as e:                  
        logger.warning(f"Prompt logging failed (non-fatal): {e}")

    normalized = _normalize_response(agent_fn(question))                                    #Calls the selected agent with the user's question and converts its response into a dictionary structure.
    latency_seconds = round(time.monotonic() - start_time, 3)                               #Calculates the total time taken to process the question, from the start of route_question() until the agent response is received.

    # Log KPIs for this query — feeds the Prove Impact dashboard
    try:
        log_query_metrics(
            question=question,
            category=category,
            routing_confidence=confidence,
            sources=normalized["sources"],
            answer_text=normalized["text"],
            latency_seconds=latency_seconds,
        )
    except Exception as e:
        logger.warning(f"Metrics logging failed (non-fatal): {e}")

    return normalized

# Standalone terminal interface for testing the supervisor. doesnt execute in normal program execution
#however , gets executed when suprvisor.py file is executed independently in terminal. it is mainly for testing the working of individual file
if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    print("=== Intersnack Multi-Agent Assistant ===")

    while True:

        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = route_question(question)

        print("\nAnswer:")
        print(answer["text"])