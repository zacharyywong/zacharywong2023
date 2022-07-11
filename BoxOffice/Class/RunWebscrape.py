from BoxOfficeWebScrape import *
import random
from datetime import datetime
import sys
import subprocess

yearList = [2022, 2021]
workBookName = "DecayCurveData-{date}.xlsx"
sheetNameDaily = "DailyMovieData"
sheetNameYear = "{year}Summary.xlsx"
holidayList = ["COVID-19 Pandemic", "Memorial Day", "Independence Day", "Easter Sunday", "Presidents' Day",
               "Christmas Day",  "New Year's Eve", "New Year's Day", "MLK Day", "Halloween", "Indig. Peoples' Day",
               "Thanksgiving", "Labor Day"]
sleepTime = random.randrange(4, 7)

def installPackages():
    packages = ["pandas", "numpy", "xlwt", "wheel", "html5lib", "bs4", "openpyxl", "selenium", "webdriver-manager"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])  # import data libraries

def run():
    installPackages()
    webScrape = BoxOfficeWebScrape(yearList, workBookName, sheetNameYear, sheetNameDaily, holidayList, sleepTime)
    webScrape.run()

if __name__ == '__main__':
    startNow = datetime.now()
    run()
    endNow = datetime.now()
    elapsedTime = endNow - startNow
    print("Total Time Elapsed: " + str(elapsedTime))
# result.head()
