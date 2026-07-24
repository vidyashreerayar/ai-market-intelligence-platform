from sqlalchemy import text
from database.connection import engine


class DatabaseLoader:

    def __init__(self):
        self.engine = engine

    def load_dataframe(self, df, table_name):

        # Duplicate check for news articles
        if table_name == "news_articles":
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT url FROM news_articles"))
                existing_urls = {row[0] for row in result}

            df = df[~df["url"].isin(existing_urls)]

            if df.empty:
                print("No new articles to load.")
                return 0

        # Duplicate check for potato prices
        elif table_name == "potato_prices":
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT year FROM potato_prices"))
                existing_years = {row[0] for row in result}

            df = df[~df["year"].isin(existing_years)]

            if df.empty:
                print("No new potato prices to load.")
                return 0

        # Load data into PostgreSQL
        df.to_sql(
            table_name,
            self.engine,
            if_exists="append",
            index=False
        )

        print(f"Successfully loaded {len(df)} rows into {table_name}.")
        return len(df)


if __name__ == "__main__":
    from etl.extract import PricingExtractor
    from etl.transform import PricingTransformer

    extractor = PricingExtractor()
    raw_data = extractor.extract()

    transformer = PricingTransformer()
    df = transformer.transform(raw_data)

    loader = DatabaseLoader()
    inserted = loader.load_dataframe(df, "potato_prices")

    print(f"Inserted {inserted} rows.")