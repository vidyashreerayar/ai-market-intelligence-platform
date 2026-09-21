import requests
import pandas as pd


class PricingExtractor:                                             #class which can be called later to extract prices from eurostat url
    def __init__(self):                                             # contructor method
        self.url = (                                                #constructor parameter, it stores eurostat url in this cast along 
            "https://ec.europa.eu/eurostat/api/dissemination/"      #with other specific parameter values such as language, currency etc
            "statistics/1.0/data/apri_ap_crpouta"
            "?lang=EN"
            "&geo=DE"
            "&prod_veg=05120000"
            "&currency=EUR"
        )       

    def extract(self):                                              #method to extract the url
        response = requests.get(self.url)                           #send api request to eurostat url with all the params mentioned inside self.url in the above contructor method.
        response.raise_for_status()                                 #checks whether the request succeeded

        data = response.json()                                      #takes eurostat json format response and converts to python format

        return data                                                 #returns the converted python format data

# Standalone test: runs only when this file is run directly
if __name__ == "__main__":                                          # Runs only when this file is run directly
    extractor = PricingExtractor()                                  # Create a pricing extractor object

    data = extractor.extract()                                      # Get the raw pricing data from Eurostat

    print("Years:")                                                 # Label the year information
    print(data["dimension"]["time"]["category"]["index"])           # Show which price-value position belongs to each year

    print("\nValues:")                                              # Label the price information
    print(data["value"])                                            # Show the actual price values from Eurostat