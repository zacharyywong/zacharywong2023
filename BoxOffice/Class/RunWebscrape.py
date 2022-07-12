# This script uses the BoxOfficeWebScrape Class script to pull and clean data from Box Office Mojo
# This is the developer interface script: Use this script to customize which years to pull from,
# how to name the Excel sheets, and add a Holiday to remove from the Date column in the Daily data
# It will generate the summary data sheet for every year and all the daily data for all titles in another sheet

# Import packages
from BoxOfficeWebScrape import *
import random
from datetime import datetime
import sys
import subprocess

# TODO: DEVELOPER CAN CHANGE

# Which years to pull data from
yearList = [2022, 2021]

# Name of the Excel workbook - {date} will be modified to today's date - can be moved within string but keep {} format
workBookName = "DecayCurveData-{date}.xlsx"

# Name of the Excel Sheets - {year} is the year of the summarized data for the title -
# can be moved within string but keep {} format
sheetNameDaily = "DailyMovieData"
sheetNameYear = "{year}Summary.xlsx"

# All holidays to detect which will be cleaned from the "Date" column in the Daily Movie Data Tab
# Ensure every holiday is spelled exactly as raw data
holidayList = ["COVID-19 Pandemic", "Memorial Day", "Independence Day", "Easter Sunday", "Presidents' Day",
               "Christmas Day", "New Year's Eve", "New Year's Day", "MLK Day", "Halloween", "Indig. Peoples' Day",
               "Thanksgiving", "Labor Day"]

# If the website overload error message comes up - a potential solution is to increase the range of seconds
# the program sleeps for in between commands
sleepTime = random.randrange(4, 7)

# TODO: END OF CUSTOMIZABLE VARIABLES


# Install all packages needed to webscrape
def installPackages():
    packages = ["pandas", "IPython", "numpy", "xlwt", "wheel", "html5lib", "bs4", "openpyxl", "selenium",
                "webdriver-manager"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])  # import data libraries


# call WebScrape class and run
def run():
    webScrape = BoxOfficeWebScrape(yearList, workBookName, sheetNameYear, sheetNameDaily, holidayList, sleepTime)
    webScrape.run()


# Install all packages, keep track of elapsed time
if __name__ == '__main__':
    installPackages()
    startNow = datetime.now()
    run()
    endNow = datetime.now()
    elapsedTime = endNow - startNow
    print("Total Time Elapsed: " + str(elapsedTime))
