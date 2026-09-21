# Import database tools and LangChain's tool decorator
from sqlalchemy import text
from langchain_core.tools import tool
from database.connection import engine

# Retrieve the latest news articles from the news_articles table
@tool
def get_latest_news(limit: int = 5) -> str:
    """
    Fetch the latest news articles from the database.
    """
    # Define the SQL query to fetch the most recent articles
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
    # Execute the query and convert each database row into a dictionary
    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit})
        articles = [dict(row._mapping) for row in result]
    # Return a message if no articles were found
    if not articles:
        return "No news articles found."
    # Format the retrieved articles into readable text
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
    # Return all formatted articles as one text block
    return "\n".join(output)

# Retrieve historical potato prices as structured data for charts
def get_potato_prices_data() -> list[dict]:
    """
    Fetch historical potato prices as structured numeric data.
    Returns:
    [
        {"year": 2000, "price_eur_per_100kg": 6.14},
        ...
    ]
    """
    # Define the SQL query to retrieve prices ordered by year
    query = text("""
        SELECT
            year,
            price_eur_per_100kg
        FROM potato_prices
        ORDER BY year
    """)
    # Execute the query and convert the results into numeric dictionaries
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
    # Return the structured price data
    return prices

# Retrieve historical potato prices as readable text for the LLM
@tool
def get_potato_prices() -> str:
    """
    Fetch historical potato prices from the database.
    """
    # Get the historical potato prices from the database
    prices = get_potato_prices_data()
    # Return a message if no price data was found
    if not prices:
        return "No potato price data found."
    # Format each year's price into readable text
    output = []

    for row in prices:
        output.append(
            f"Year: {row['year']}, Price: €{row['price_eur_per_100kg']:.2f} per 100 kg"
        )
    # Return all price records as one text block
    return "\n".join(output)

# Run both database tools directly for testing
if __name__ == "__main__":
    print(get_latest_news.invoke({"limit": 5}))
    print()
    print(get_potato_prices.invoke({}))