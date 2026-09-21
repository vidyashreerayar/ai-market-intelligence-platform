import os                                                               # Access environment variables
import requests                                                         # Make HTTP API requests
import pandas as pd                                                     # Store and process news data
from dotenv import load_dotenv                                          # Load variables from .env file

load_dotenv()                                                           # Load .env variables into the environment


class NewsAPIExtractor:                                                 # Define the NewsAPI extraction component
    BASE_URL = "https://newsapi.org/v2/everything"                      # Address used to request news from NewsAPI

    def __init__(self):                                                 # Initialize the extractor object(constructor)
        self.api_key = os.getenv("NEWS_API_KEY")                        # Read the API key from environment

    def fetch_news(self, query="snacks", language="en", page_size=20):  # Define a function for getting news, with default search settings
        params = {
            "q": query,                                                 # What topic to search for
            "language": language,                                       # Language of the articles
            "pageSize": page_size,                                      # Number of articles to request
            "sortBy": "publishedAt",                                    # Show the newest articles first
            "apiKey": self.api_key,                                     # API key used to access NewsAPI
        }

        response = requests.get(self.BASE_URL, params=params)           # fetch news from newsAPI
        response.raise_for_status()                                     # Stop and report an error if the news request failed

        articles = response.json().get("articles", [])                  # Read the JSON response and convert it into Python data

        return pd.DataFrame([                                           # Create and return a table from the news articles                                  
            {
                "title": article["title"],                              # Get the article title
                "source": article["source"]["name"],                    # Get the news source name
                "published_at": article["publishedAt"],                 # Get the publication date and time
                "url": article["url"],                                  # Get the original article link
                "description": article["description"],                  # Get the article description
            }
            for article in articles                                     # Create one row for each article received
        ])




if __name__ == "__main__":                                              # Run this test only when this file is run directly
    extractor = NewsAPIExtractor()                                      # Create the component that fetches news
    

    df = extractor.fetch_news(query="potato chips")                     # Get news about potato chips

    print(df.head())                                                    # Show the first 5 rows to check the extracted dat