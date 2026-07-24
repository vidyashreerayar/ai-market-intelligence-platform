import pandas as pd


class NewsTransformer:

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop_duplicates(subset=["url"])
        df = df.dropna(subset=["title"])
        df["description"] = df["description"].fillna("")
        df["published_at"] = pd.to_datetime(df["published_at"])

        return df

class PricingTransformer:
    def transform(self, data):
        years = data["dimension"]["time"]["category"]["index"]
        values = data["value"]

        records = []

        for year, idx in years.items():
            records.append({
                "year": int(year),
                "price_eur_per_100kg": values.get(str(idx))
            })

        df = pd.DataFrame(records)
        return df.sort_values("year").reset_index(drop=True)

if __name__ == "__main__":
    from extract import PricingExtractor

    extractor = PricingExtractor()
    data = extractor.extract()

    transformer = PricingTransformer()
    df = transformer.transform(data)

    print(df.head())
    print()
    print(df.tail())