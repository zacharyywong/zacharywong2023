from BoxOfficeWebScrape import *
import random
from datetime import datetime
from time import sleep

packages = ["pandas", "numpy", "xlwt", "wheel", "html5lib", "bs4", "openpyxl", "selenium", "webdriver-manager"]
yearList = [2022]
urlYearly = 'https://www.boxofficemojo.com/year/?ref_=bo_nb_hm_secondarytab'
sheetNameDaily = "DailyMovieData"
sheetNameYear = "{year}Summary.xlsx"
sleepTime = random.randrange(4, 7)

def installPackages():
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])  # import data libraries


def cleanDailyTable(webScrape):
    global dfDailyTable
    dfDailyTable = webScrape.cleanTable(dfDailyTable)
    dfDailyTable = webScrape.renameDailyTable(dfDailyTable)
    dfDailyTable = webScrape.reorderDailyTable(dfDailyTable)
    dfDailyTable = webScrape.cleanDailyDistributor(dfDailyTable)
    dfDailyTable = webScrape.cleanDate(dfDailyTable)
    return dfDailyTable


def run():
    installPackages()
    webScrape = BoxOfficeWebScrape(urlYearly)

    for year in yearList:
        try:
            driver.get(urlYearly)
        except:
            print("Cannot access {url}...quitting now").format(url=urlYearly)
        webScrape.runYear(year, sheetNameYear)
        sleep(sleepTime)

    global dfDailyTable
    print(dfDailyTable)
    webScrape.writetoExcel(dfDailyTable, sheetNameDaily)
    dfDailyTable = cleanDailyTable()

    print(dfDailyTable)
    webScrape.writetoExcel(dfDailyTable, sheetNameDaily)
    wb.save(filename=totalFileName)


if __name__ == '__main__':
    startNow = datetime.now()
    run()
    endNow = datetime.now()
    elapsedTime = endNow - startNow
    print("Total Time Elapsed: " + str(elapsedTime))
# result.head()
