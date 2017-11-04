# from flask import Flask, url_for, render_template
# from app import app

from brewerydb.brewerydb import BreweryDB


# API Key:  5ceb8b4ef81887489d3b65211a60fe12


class BreweryQuery:
    def __init__(self, api_key):
        self._key = api_key

    def get_alcohol_content(self):
        brew_api = BreweryDB(self._key)
        beer = brew_api.search_beer("Corona Light")
        return beer


def main():
    my_api_key = "5ceb8b4ef81887489d3b65211a60fe12"
    test = BreweryQuery(my_api_key)
    result = test.get_alcohol_content()
    print(result)


if __name__ == "__main__":
    main()
