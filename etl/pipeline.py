def run_pipeline():

    loader = DatabaseLoader()

    # ---------- News ----------
    news_extractor = NewsAPIExtractor()
    news_transformer = NewsTransformer()

    news_df = news_extractor.fetch_news(query="potato chips")
    news_df = news_transformer.clean(news_df)

    inserted = loader.load_dataframe(news_df, "news_articles")
    print(f"News: {inserted} rows loaded.")

    # ---------- Pricing ----------
    pricing_extractor = PricingExtractor()
    pricing_transformer = PricingTransformer()

    pricing_df = pricing_extractor.fetch_prices()
    pricing_df = pricing_transformer.clean(pricing_df)

    inserted = loader.load_dataframe(pricing_df, "commodity_prices")
    print(f"Pricing: {inserted} rows loaded.")