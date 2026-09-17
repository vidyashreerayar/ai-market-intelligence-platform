from etl.extract import PricingExtractor
from etl.transform import PricingTransformer, NewsTransformer
from etl.load import DatabaseLoader
from etl.indexer import NewsIndexer
from scrapers.news_api import NewsAPIExtractor

# Category mapped per query — expand as your agents need more coverage
NEWS_QUERIES = {
    "general_news": ["snacks", "Intersnack", "potato chips"],
    "competitor_retail": ["Lays", "Pringles", "Doritos", "PepsiCo snacks", "Mondelez snacks"],
    "consumer_trend": ["healthy snacking trend", "snack industry growth"],
}


def run_pipeline():

    loader = DatabaseLoader()
    indexer = NewsIndexer()
    indexer.ensure_schema()

    # ---------- News ----------
    news_extractor = NewsAPIExtractor()
    news_transformer = NewsTransformer()

    for category, queries in NEWS_QUERIES.items():
        for query in queries:
            news_df = news_extractor.fetch_news(query=query)
            news_df = news_transformer.clean(news_df)

            inserted = loader.load_dataframe(news_df, "news_articles")
            print(f"News ({query}): {inserted} rows loaded.")

            # Index ALL fetched rows (not just newly-loaded ones) — the indexer
            # does its own url-based dedup, so previously-loaded-but-unindexed
            # rows still get embedded.
            indexed = indexer.index_dataframe(news_df, category=category)
            print(f"News ({query}): {indexed} rows indexed.")

    # ---------- Pricing ----------
    pricing_extractor = PricingExtractor()
    pricing_transformer = PricingTransformer()

    raw_data = pricing_extractor.extract()
    pricing_df = pricing_transformer.transform(raw_data)

    inserted = loader.load_dataframe(pricing_df, "potato_prices")
    print(f"Pricing: {inserted} rows loaded.")
    # Note: pricing data stays structured (no embedding needed) — the pricing_agent
    # queries potato_prices directly rather than via RAG retrieval.


if __name__ == "__main__":
    run_pipeline()