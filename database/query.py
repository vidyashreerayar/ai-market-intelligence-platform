from sqlalchemy import text
from langchain_core.tools import tool
from database.connection import engine


@tool
def get_latest_news(limit: int = 5) -> str:
    """
    Fetch the latest news articles from the database.
    """

    query = text("""
        SELECT
            title,
            source,
            published_at,
            url
        FROM news_articles
        ORDER BY published_at DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit})
        articles = [dict(row._mapping) for row in result]

    if not articles:
        return "No news articles found."

    output = []

    for article in articles:
        output.append(
            f"""
Title: {article['title']}
Source: {article['source']}
Published: {article['published_at']}
URL: {article['url']}
"""
        )

    return "\n".join(output)


def get_potato_prices_data() -> list[dict]:
    """
    Fetch historical potato prices as structured numeric data.
    Returns:
    [
        {"year": 2000, "price_eur_per_100kg": 6.14},
        ...
    ]
    """

    query = text("""
        SELECT
            year,
            price_eur_per_100kg
        FROM potato_prices
        ORDER BY year
    """)

    with engine.connect() as conn:
        result = conn.execute(query)

        prices = []

        for row in result:
            prices.append(
                {
                    "year": int(row.year),
                    "price_eur_per_100kg": float(row.price_eur_per_100kg)
                }
            )

    return prices


@tool
def get_potato_prices() -> str:
    """
    Fetch historical potato prices from the database.
    """

    prices = get_potato_prices_data()

    if not prices:
        return "No potato price data found."

    output = []

    for row in prices:
        output.append(
            f"Year: {row['year']}, Price: €{row['price_eur_per_100kg']:.2f} per 100 kg"
        )

    return "\n".join(output)


if __name__ == "__main__":
    print(get_latest_news.invoke({"limit": 5}))
    print()
    print(get_potato_prices.invoke({}))