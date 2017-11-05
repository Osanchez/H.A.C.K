from flask import Flask, render_template, request

from brewerydb.brewerydb import BreweryDB


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
        output = self.get_total_alcohol_content()
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

        return total / volume


app = Flask(__name__)

api = BreweryQuery("5ceb8b4ef81887489d3b65211a60fe12")


@app.route('/', methods=['GET', 'POST'])
def get_attributes():
    if request.method == 'POST':
        beer = request.form["liquor"]
        api.add_beers(beer)
        result = str(api)
        return render_template('page1.html', A=int(result))
    else:
        return render_template('page1.html', A=int(1))


if __name__ == '__main__':
    app.debug = True
    app.run()
