import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class NewsAPIExtractor:
    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")

    def fetch_news(self, query="snacks", language="en", page_size=20):
        params = {
            "q": query,
            "language": language,
            "pageSize": page_size,
            "sortBy": "publishedAt",
            "apiKey": self.api_key,
        }

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()

        articles = response.json().get("articles", [])

        return pd.DataFrame([
            {
                "title": article["title"],
                "source": article["source"]["name"],
                "published_at": article["publishedAt"],
                "url": article["url"],
                "description": article["description"],
            }
            for article in articles
        ])


#from etl.transform import NewsTransformer

if __name__ == "__main__":
    extractor = NewsAPIExtractor()
    #transformer = NewsTransformer()

    df = extractor.fetch_news(query="potato chips")
    #cleaned_df = transformer.clean(df)

    print(df.head())