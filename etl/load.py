from sqlalchemy import text                                                 # Used to write and execute SQL queries
from database.connection import engine                                      # Import the PostgreSQL database connection


class DatabaseLoader:                                                       # Define the component that loads data into PostgreSQL

    def __init__(self):                                                     # Initialize the database loader
        self.engine = engine                                                # Store the database connection for later use

    def load_dataframe(self, df, table_name):                               # Loads a DataFrame into the specified database table                      

        # Duplicate check for news articles
        if table_name == "news_articles":
            with self.engine.connect() as conn:                             # Connect to PostgreSQL and 
                result = conn.execute(text("SELECT url FROM news_articles"))  # run the SQL query to select "url" from news_articles table                existing_urls = {row[0] for row in result}                   # Store URLs of articles that are already in the database

            df = df[~df["url"].isin(existing_urls)]                          # in the incoming data comapare with already existing data in postgre tabl and keep only articles whose URLs are not already stored

            if df.empty:                                                      # Stop if there are no new articles to load
                print("No new articles to load.")
                return 0

        # Compare incoming data values with already existing postgre value and Check which incoming price records already exist in PostgreSQL
        # Remove existing records from the incoming data and load only new price records
        elif table_name == "potato_prices":
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT year FROM potato_prices"))
                existing_years = {row[0] for row in result}

            df = df[~df["year"].isin(existing_years)]

            if df.empty:
                print("No new potato prices to load.")
                return 0

        # Load data into PostgreSQL
        # Append the new records to the specified PostgreSQL table
        df.to_sql(
            table_name,
            self.engine,
            if_exists="append",
            index=False
        )

        print(f"Successfully loaded {len(df)} rows into {table_name}.")         # Show how many new records were loaded
        return len(df)                                                          # Return the number of records that were loaded

# Standalone test: extract, transform, and load potato price data into PostgreSQL
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