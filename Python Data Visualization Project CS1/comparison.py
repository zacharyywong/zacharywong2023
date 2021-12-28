# Author: Zachary Wong
# Date: 8/18/2020
# Purpose: Reads in the original data file and write out new files sorted by latitude, population, and name.

from city import City
from quicksort import *


# Checkpoint
# Open the data file in the read and write format

fr_ref = open("world_cities.txt", "r")
fw_ref = open("cities_out.txt", "w")


# Create a list for each location, create an object in the City class, and append it to the list

blist = []
for line in fr_ref:
    line = line.strip()
    wlist = line.split(",")
    object = City(wlist[0], wlist[1], wlist[2], wlist[3], wlist[4], wlist[5])
    blist.append(object)


# For each object in the city class, put the returned string into separate lines

for object in blist:
    fw_ref.write(str((object)) + "\n")


# Close Files
fr_ref.close()
fw_ref.close()


# Post-Checkpoint
# read in the original data file and open the other three files that will give sorted data by latitude, population, and
# name

fr_ref = open("world_cities.txt", "r")
fw_ref_pop = open("cities_population.txt", "w")
fw_ref_lat = open("cities_latitude.txt", "w")
fw_ref_alpha = open("cities_alpha.txt", "w")


# Comparison function for population

def compare_population(citya, cityb):
    return citya.pop >= cityb.pop


# Comparison function for name

def compare_name(citya, cityb):
    return citya.name.lower() <= cityb.name.lower()


# Comparison function for latitude

def compare_lat(citya, cityb):
    return citya.lat <= cityb.lat


# Create a list for each location, create an object in the City class, and append it to the list

blist = []
for line in fr_ref:
    line = line.strip()
    wlist = line.split(",")
    object = City(wlist[0], wlist[1], wlist[2], wlist[3], wlist[4], wlist[5])
    blist.append(object)


# sort by population and write it out in "cities_population.txt"

sort(blist, compare_population)
for object in blist:
    fw_ref_pop.write(str(object) + "\n")


# sort by latitude and write it out in "cities_latitude.txt"

sort(blist, compare_lat)
for object in blist:
    fw_ref_lat.write(str(object) + "\n")


# sort by name and write it out in "cities_alpha.txt"

sort(blist, compare_name)
for object in blist:
    fw_ref_alpha.write(str(object) + "\n")


# close all files

fr_ref.close()
fw_ref_pop.close()
fw_ref_lat.close()
fw_ref_alpha.close()


