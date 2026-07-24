import requests
import pandas as pd


class PricingExtractor:
    def __init__(self):
        self.url = (
            "https://ec.europa.eu/eurostat/api/dissemination/"
            "statistics/1.0/data/apri_ap_crpouta"
            "?lang=EN"
            "&geo=DE"
            "&prod_veg=05120000"
            "&currency=EUR"
        )       

    def extract(self):
        response = requests.get(self.url)
        response.raise_for_status()

        data = response.json()

        return data

if __name__ == "__main__":
    extractor = PricingExtractor()

    data = extractor.extract()

    print("Years:")
    print(data["dimension"]["time"]["category"]["index"])

    print("\nValues:")
    print(data["value"])