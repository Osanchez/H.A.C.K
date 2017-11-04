# from flask import Flask, url_for, render_template
# from app import app

from brewerydb.brewerydb import BreweryDB
# API Key:  5ceb8b4ef81887489d3b65211a60fe12


class BreweryQuery:
    def __init__(self, api_key):
        self._key = api_key
        self._api = self.get_api()

    def get_api(self):
        return BreweryDB(self._key)

    def get_alcohol_content(self, beer_name):
        print(beer_name)
        arguments = beer_name.split(" ")  # String to array of words
        beers = self._api.search_beer(arguments[0])  # give api search method first word of string
        if len(arguments) > 1:
            beer = self.refined_search(arguments[1::], beers)
            return beer
        else:
            return beers

    def refined_search(self, arguments, search_array):
        updated_list = None
        for i in arguments:
            updated_list = filter(lambda k: i in k.name, search_array)
        return updated_list


def main():
    my_api_key = "5ceb8b4ef81887489d3b65211a60fe12"
    test = BreweryQuery(my_api_key)
    result = test.get_alcohol_content("Corona Light")

    for i in result:
        print("Alcohol Content: " + i.abv + "%")


if __name__ == "__main__":
    main()
