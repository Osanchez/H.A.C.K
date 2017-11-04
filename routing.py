# from flask import Flask, url_for, render_template
# from app import app

from brewerydb.brewerydb import BreweryDB
# API Key:  5ceb8b4ef81887489d3b65211a60fe12


def refined_search(arguments, search_array):  # Static Method
    updated_list = None  # Declares a variable that will be updated after each search
    for i in arguments:  # run filters for each of the remaining arguments
        updated_list = filter(lambda k: i in k.name, search_array)  # filtered results
    return updated_list  # return final results


class BreweryQuery:
    def __init__(self, api_key):
        self._key = api_key  # store api key privately
        self._api = self.get_api()  # initialize the API calling object

    def get_api(self):  # returns API calling object
        return BreweryDB(self._key)

    def get_alcohol_content(self, beer_name):
        arguments = beer_name.split(" ")  # arguments to array of strings
        # API search method takes words separated by white spaces as separate arguments. Because of this, the
        # search method call will return all beers that contain any of the words in the argument.
        # to compensate, only the first word in the argument is given, before another refined search method is called
        beers = self._api.search_beer(arguments[0])  # give api search method first word of argument
        if len(arguments) > 1:  # If the argument only contains one word there is no need to run the refined search
            beer = refined_search(arguments[1::], beers)  # rest of the arguments, first search results
            return beer  # returns finalized results
        else:
            return beers  # returns all possible results


def main():
    my_api_key = "5ceb8b4ef81887489d3b65211a60fe12"  # 400 api calls daily
    test = BreweryQuery(my_api_key)  # creates a BreweryQuery object and initialized it to variable named test
    # TODO: Throw beer names here to test search method.
    result = test.get_alcohol_content("Corona Light")  # Calls method from the BrewerQuery Object

    # for each item in result set print name of beer object and alcohol content of beer object
    for i in result:
        print("Beer Name: " + i.name)
        print("Alcohol Content: " + i.abv + "%")
        print


if __name__ == "__main__":
    main()
