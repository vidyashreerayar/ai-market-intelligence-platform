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

logger = logging.getLogger(__name__)

# Maps intent category -> your existing agent functions
AGENT_MAP = {
    "commodity_price": pricing_agent,
    "competitor_retail": market_agent,
    "consumer_trend": trend_agent,
    "general_news": news_agent,
}

INTENT_DESCRIPTIONS = {
    "commodity_price": "Raw material prices, commodity trends, potato/oil costs, inflation, currency (EUR), '100kg' pricing",
    "competitor_retail": "Competitors, brands, market share, product launches (Lays, Pringles, Doritos, PepsiCo, Kellogg, Mondelez)",
    "consumer_trend": "Consumer preferences, trending topics, growth, industry demand, future outlook, behavior",
    "general_news": "Anything else — general news, or queries that don't clearly fit the other categories",
}

CONFIDENCE_THRESHOLD = 0.6

SYSTEM_PROMPT = f"""You are an intent classifier for a snack industry business intelligence assistant.
Classify the user's question into ONE of these categories:

{json.dumps(INTENT_DESCRIPTIONS, indent=2)}

Return ONLY valid JSON in this exact format:
{{"category": "<category_name>", "confidence": <0.0-1.0>}}

Be honest about confidence — if the question is ambiguous or doesn't clearly match a category, use a low confidence score rather than guessing.
"""

_groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])


def _normalize_response(result):
    if isinstance(result, dict):
        return {
            "text": result.get("text", ""),
            "chart_data": result.get("chart_data"),
            "chart_title": result.get("chart_title"),
            "chart_type": result.get("chart_type"),
            "sources": result.get("sources", [])
        }

    return {
        "text": result,
        "chart_data": None,
        "chart_title": None,
        "chart_type": None,
        "sources": []
    }


def classify_intent(question: str) -> dict:
    """Returns {'category': str, 'confidence': float}. Falls back to general_news on any error."""
    try:
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
    except Exception as e:
        logger.warning(f"Intent classification failed ({e}), falling back to general_news")
        return {"category": "general_news", "confidence": 0.0}


def route_question(question: str):
    start_time = time.monotonic()

    result = classify_intent(question)
    category = result["category"]
    confidence = result["confidence"]

    if confidence < CONFIDENCE_THRESHOLD:
        logger.info(f"Low confidence ({confidence:.2f}) for '{question}' — using general_news fallback")
        category = "general_news"

    agent_fn = AGENT_MAP.get(category, news_agent)
    logger.info(f"Routed to '{category}' (confidence {confidence:.2f}): {agent_fn.__module__}")

    # Log the classifier prompt used for this query — tracks prompt changes over time
    try:
        log_prompt(question=question, category=category, system_prompt=SYSTEM_PROMPT)
    except Exception as e:
        logger.warning(f"Prompt logging failed (non-fatal): {e}")

    normalized = _normalize_response(agent_fn(question))
    latency_seconds = round(time.monotonic() - start_time, 3)

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