# Author: Zachary Wong
# Date: 8/18/2020
# Purpose: Define a City class, read in the data, and write out the data in a text file (cities.out.txt)

# This is the city class which returns a string of information relating to one location

class City:

    # Convert the parameters into the right format

    def __init__(self, ccode, name, region, population, latitude, longitude):
        self.ccode = str(ccode)
        self.name = str(name)
        self.region = str(region)
        self.pop = int(population)
        self.lat = float(latitude)
        self.long = float(longitude)

    # return a string of the name, population, latitude, and longitude

    def __str__(self):
        return(str(self.name) + "," + str(self.pop) + "," + str(self.lat) + "," + str(self.long))



