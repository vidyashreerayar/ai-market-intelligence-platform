import pandas as pd


class NewsTransformer:                                              #class to transform the incoming raw data from articles

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:              #function to clean the incoming raw data, defining the the incoming and cleaned data both will be dataframes
        df = df.drop_duplicates(subset=["url"])                     #removes any duplicate urls and maintains only the unique urls
        df = df.dropna(subset=["title"])                            #removes and article with title NaN(not blank) values
        df["description"] = df["description"].fillna("")            #replaces description of articles with NaN values with blank text, so it can be considered
        df["published_at"] = pd.to_datetime(df["published_at"])     #converts the date info to a datetime format so the format is even throughout

        return df                                                   #the cleaned dataframe in returned

class PricingTransformer:                                           # class to handle transformation of Eurostat price data
    def transform(self, data):                                      # Method to convert raw Eurostat data into a structured Pandas DataFrame
        years = data["dimension"]["time"]["category"]["index"]      # Get the year-to-position mapping from the Eurostat data
        values = data["value"]                                      # Get the actual price values from the Eurostat data

        records = []                                                # Create an empty list to store the year and price records

        for year, idx in years.items():                             # Go through each year and its corresponding position
            records.append({                                        # Add one year-and-price new record to the list
                "year": int(year),                                  # Store the year as an integer instead of text
                "price_eur_per_100kg": values.get(str(idx))         # Get the price at this position and store it in euros per 100 kg
            })

        df = pd.DataFrame(records)                                  # Convert the list of year-and-price records into a Pandas DataFrame
        return df.sort_values("year").reset_index(drop=True)        # Sort the DataFrame by year and reset the row numbers

# Standalone test: get Eurostat data, transform it, and display the first and last rows to verify the result
if __name__ == "__main__":
    from extract import PricingExtractor

    extractor = PricingExtractor()
    data = extractor.extract()

    transformer = PricingTransformer()
    df = transformer.transform(data)

    print(df.head())
    print()
    print(df.tail())