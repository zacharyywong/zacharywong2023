# Author: Zachary Wong
# Date: 8/18/2020
# Purpose: Visualize the cities according to the top 50 most populated cities

from cs1lib import *


# Open the file with data sorted by population

img = load_image("world.png")
fr_ref_pop = open("cities_population.txt", "r")


# Constants

WINDOW_HEIGHT = 360
WINDOW_LENGTH = 720
CENTER_X = 360
CENTER_Y = 180


# Global Variabes

begin = False
frame = 1
index = 0
n = 1
blist = []


# Calculate the location of the city and return the x and y positions of the cities on the image. Takes a list and the
# associated index of the list as parameters.

def calculate_location(blist, i):

    # Width and height scales account for the fact that the image in pixels is 2 times wider than 360
    # and the height is 2 times longer than 180 degrees

    width_scale = 2
    height_scale = 2

    # Grabs the longitude from blist and calculates the distance from the center of the image

    distance_x = float(blist[i][3]) * width_scale
    x = CENTER_X + distance_x
    distance_y = abs(float(blist[i][2]) * height_scale)

    # Accounts for the fact that measuring the latitude on the canvas is the opposite of longitude calculations

    if float(blist[i][2]) > 0:
        y = CENTER_Y - distance_y
    elif float(blist[i][2]) < 0:
        y = CENTER_Y + distance_y
    else:
        y = CENTER_Y
    return x, y


# Draw a rectangle for the top 50 most populated cities

def draw(x, y):
    if n <= 50:
        set_fill_color(1, 0, 1)
        set_stroke_color(0, 0, 0)
        draw_rectangle(x, y, 5, 5)


# Draw the image and the cities

def main():
    global begin, frame, index, blist, n

    # Only draw the image once and append the data sorted by population into a list, splitting each line by commas

    if begin == False:
        draw_image(img, 0, 0)
        begin = True
        for line in fr_ref_pop:
            wlist = line.split(",")
            blist.append(wlist)

    # Show the cities one by one in order of most populated

    if frame % 40 == 0 and n <= 50:
        x, y = calculate_location(blist, index)
        draw(x, y)
        index += 1
        n += 1
    frame += 1


start_graphics(main, height = 360, width = 720)
fr_ref_pop.close()