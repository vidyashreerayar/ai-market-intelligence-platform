from agents.news_agent import answer_question as news_agent
from agents.market_agent import answer_question as market_agent
from agents.trend_agent import answer_question as trend_agent
from agents.pricing_agent import answer_question as pricing_agent


def _normalize_response(result):
    if isinstance(result, dict):
        return {
            "text": result.get("text", ""),
            "chart_data": result.get("chart_data"),
            "chart_title": result.get("chart_title"),
            "chart_type": result.get("chart_type")
        }

    return {
        "text": result,
        "chart_data": None,
        "chart_title": None,
        "chart_type": None
    }


def route_question(question: str):

    q = question.lower()

    market_keywords = [
        "competitor",
        "competition",
        "market",
        "brand",
        "launch",
        "lays",
        "pringles",
        "doritos",
        "pepsico",
        "kellogg",
        "mondelez"
    ]

    trend_keywords = [
        "trend",
        "trending",
        "consumer",
        "popular",
        "emerging",
        "growth",
        "industry",
        "preference",
        "behavior",
        "demand",
        "future"
    ]

    pricing_keywords = [
        "price",
        "pricing",
        "potato",
        "cost",
        "costs",
        "raw material",
        "commodity",
        "inflation",
        "eur",
        "100 kg"
    ]

    if any(keyword in q for keyword in pricing_keywords):
        return _normalize_response(pricing_agent(question))

    if any(keyword in q for keyword in trend_keywords):
        return _normalize_response(trend_agent(question))

    if any(keyword in q for keyword in market_keywords):
        return _normalize_response(market_agent(question))

    return _normalize_response(news_agent(question))


if __name__ == "__main__":

    print("=== Intersnack Multi-Agent Assistant ===")

    while True:

        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = route_question(question)

        print("\nAnswer:")
        print(answer["text"])