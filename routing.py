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
        self.beers = []

    def __str__(self):
        output = ''
        output += "Total Alcohol Content: " + str(self.get_total_alcohol_content())
        return output

    def get_api(self):  # returns API calling object
        return BreweryDB(self._key)

    def get_beers(self):
        return self.beers

    def add_beers(self, beer):
        try:
            beers_array = self.get_alcohol_content(beer)
            if len(beers_array) == 1:
                self.beers.append(beers_array[0])
                return
            else:
                print("Please be more specific with beer name")
            # else:
                # counter = 0
                # for i in beers_array:
                    # print("[" + str(counter) + "] " + i.name)
                    # counter += 1
            # print
            # choice = input("Please Select Beer: ")
            # self.beers.append(beers_array[choice])
        except TypeError:
            return

    def get_alcohol_content(self, beer_name):
        arguments = beer_name.split(" ")  # arguments to array of strings
        # API search method takes words separated by white spaces as separate arguments. Because of this, the
        # search method call will return all beers that contain any of the words in the argument.
        # to compensate, only the first word in the argument is given, before another refined search method is called
        try:
            beers = self._api.search_beer(arguments[0])  # give api search method first word of argument
        except KeyError:
            print("Invalid Entry")
            return

        if len(arguments) > 1:  # If the argument only contains one word there is no need to run the refined search
            beer = refined_search(arguments[1::], beers)  # rest of the arguments, first search results
            return beer  # returns finalized results
        else:
            if len(beers) == 1:
                return beers
            else:
                return beers  # returns all possible results

    def get_total_alcohol_content(self):  # MAGIC FORMULA
        total = 0
        volume = 0

        for x in self.beers:
            total += float(x.abv) * 12
            volume += 12

        return total/volume


def main():  # Testing
    my_api_key = "5ceb8b4ef81887489d3b65211a60fe12"  # 400 api calls daily

    # creates a object that communicates with the database using PyBreweryAPI
    # TODO: Flask will make functions calls using API_Object
    API_Object = BreweryQuery(my_api_key)  # creates a BreweryQuery object and initialized it to variable named test

    # These are the function calls you will work with
    # API_Object.add_beers("Corona Light")  # Searches for beer and appends matching result to a list of beers
    # result = API_Object # printing object calculates alcohol content total of all drinks that were searched for
    # print(result) # prints the results

if __name__ == "__main__":
    main()
