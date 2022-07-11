from openpyxl import Workbook
import pandas as pd
import numpy as np
from datetime import datetime
from time import sleep
import pytz
from openpyxl.utils.dataframe import dataframe_to_rows

# import selenium/webscraping libs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Access webdriver for Chrome
driver_path = '/Users/zacharywong/Downloads/chromedriver'
service = Service(driver_path)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
waitTime = 10
boolColumnDropIndex = 10

# keep track of day/time
est = pytz.timezone('US/Eastern')
fmt = '%d-%m-%Y'
now = datetime.now()
now = now.astimezone(est).strftime(fmt)
print("day/time: " + now)

# excel
path = "/Users/zacharywong/github/zacharywong2023/BoxOffice/"
wb = Workbook()

urlYearly = 'https://www.boxofficemojo.com/year/?ref_=bo_nb_hm_secondarytab'
dailyColumns = ["Date", "DOW", "Rank", "Daily", "%+/-YR", "%+/-LW", "Theaters", "Avg", "To Date", "Day", "Title",
                "Genre", "Distributor"]
yearlyColumns = ["Rank", "Release", "Gross", "Max Th", "Opening", "% of Total", "Open Th", "Open", "Close",
                 "Distributor"]

dfDailyTable = pd.DataFrame()
dfYearlyTable = pd.DataFrame()


class BoxOfficeWebScrape:
    def __init__(self, yearList, workbookName, sheetNameYear, sheetNameDaily, holidayList, sleepTime):
        self.yearList = yearList
        self.workBookName = workbookName
        self.totalFileName = self.workBookName.format(date=now)
        wb.save(self.totalFileName)

        self.sheetNameYear = sheetNameYear
        self.sheetNameDaily = sheetNameDaily
        self.holidayList = holidayList

        self.sleepTime = sleepTime

    def writetoExcel(self, df, sheetName):
        ws = wb.create_sheet()
        ws.title = sheetName
        rows = dataframe_to_rows(df, index=False, header=True)
        for row in rows:
            ws.append(row)
        wb.save(self.totalFileName)

    # Filter by In Year Releases and Wide Releases
    def clickFilters(self):
        XPATHinYear = "/html/body/div[1]/main/div/div/div[1]/div[2]/span/form/span/select"
        XPATHwideRelease = "/html/body/div[1]/main/div/div/div[1]/div[3]/span/form/span/select"
        sleep(self.sleepTime)

        try:
            filterInYearSelect = Select(driver.find_element(By.XPATH, XPATHinYear))
        except:
            WebDriverWait(driver, waitTime).until(EC.presence_of_element_located((By.XPATH, XPATHinYear)))
            filterInYearSelect = Select(driver.find_element(By.XPATH, XPATHinYear))

        filterInYearSelect.select_by_visible_text("In-year releases")
        sleep(self.sleepTime)

        try:
            filterwidereleaseSelect = Select(driver.find_element(By.XPATH, XPATHwideRelease))
        except:
            WebDriverWait(driver, waitTime).until(EC.presence_of_element_located((By.XPATH, XPATHwideRelease)))
            filterwidereleaseSelect = Select(driver.find_element(By.XPATH, XPATHwideRelease))

        filterwidereleaseSelect.select_by_visible_text("Wide releases")

    def getMovieLink(self, index):
        # //*[@id="table"]/div/table[2]/tbody/tr[2]/td[2]/a
        XPATHMovie = "//*[@id='table']/div/table[2]/tbody/tr[{index}]/td[2]/a".format(index=index)
        try:
            movie = driver.find_element(By.XPATH, XPATHMovie)
        except:
            WebDriverWait(driver, waitTime).until(EC.presence_of_element_located((By.XPATH, XPATHMovie)))
            movie = driver.find_element(By.XPATH, XPATHMovie)
        return movie, movie.text

    def getRowColumnNumber(self):
        adjustForHeader = 1
        rowXPATH = "//*[@id='table']/div/table[2]/tbody/tr"
        colXPATH = "//*[@id='table']/div/table[2]/tbody/tr[1]/th"
        colNumber = 0
        rowNumber = len(driver.find_elements(By.XPATH, rowXPATH)) - adjustForHeader
        return rowNumber, colNumber

    def getTableData(self):
        tempResult = pd.read_html(driver.page_source, flavor='html5lib')[1]
        return tempResult

    @staticmethod
    def cleanTable(df):
        for column in df:
            df[column] = df[column].replace(['-'], np.nan)
        df = df.dropna(axis=1, how='all')
        df = df.drop(df.columns[[boolColumnDropIndex]], axis=1)
        return df

    @staticmethod
    def renameYearlyTable(df):
        df.columns = yearlyColumns
        return df

    @staticmethod
    def renameDailyTable(df):
        df.columns = dailyColumns
        return df

    @staticmethod
    def reorderDailyTable(df):
        colsOrdered = ["Distributor", "Title", "Genre", "Date", "DOW", "Rank", "Daily", "%+/-YR", "%+/-LW", "Theaters",
                       "Avg", "To Date", "Day"]
        df = df[colsOrdered]
        return df

    def cleanDailyDistributor(self, df):
        df["Distributor"] = df["Distributor"].str.split('\n').str[0]
        return df

    def cleanDate(self, df):
        for holiday in self.holidayList:
            df["Date"] = df["Date"].str.split(holiday).str[0]

        return df

    def getDailyMovieData(self, movieTitle):
        rowNumber, colNumber = self.getRowColumnNumber()
        indexList = []
        XPATHGenre = "//*[@id='a-page']/main/div/div[3]/div[4]/div[6]/span[2]"
        XPATHDistributor = "//*[@id='a-page']/main/div/div[3]/div[4]/div[1]/span[2]"
        #            value = (driver.find_element(By.XPATH, XPATHValue)).text
        for number in range(0, rowNumber):
            indexList.append(number)

        tempResult = self.getTableData()
        tempResult["Title"] = movieTitle
        tempResult["Genre"] = (driver.find_element(By.XPATH, XPATHGenre)).text
        tempResult["Distributor"] = (driver.find_element(By.XPATH, XPATHDistributor)).text
        return tempResult

    def getAllDailyData(self, rowNumber):
        print("Number of Movies:" + str(rowNumber))
        index = 2
        while index < rowNumber + 2:
            tempResult = None
            print("index: " + str(index))
            startNow = datetime.now()
            movieDriver, movieTitle = self.getMovieLink(index)
            print(movieTitle)
            movieDriver.click()
            self.getRowColumnNumber()
            global dfDailyTable
            try:
                tempResult = self.getDailyMovieData(movieTitle)
            except:
                print("cannot read movies further - most likely website overload")

            dfDailyTable = pd.concat([dfDailyTable, tempResult])
            index += 1

            sleep(self.sleepTime)
            driver.execute_script("window.history.go(-1)")
            sleep(self.sleepTime)
            endNow = datetime.now()
            timeElapsed = endNow - startNow
            print("time elapsed: " + str(timeElapsed))

    def cleanYearlyTable(self):
        global dfYearlyTable
        dfYearlyTable = self.cleanTable(dfYearlyTable)
        dfYearlyTable = self.renameYearlyTable(dfYearlyTable)

    def cleanDailyTable(self):
        global dfDailyTable
        dfDailyTable = self.cleanTable(dfDailyTable)
        dfDailyTable = self.renameDailyTable(dfDailyTable)
        dfDailyTable = self.reorderDailyTable(dfDailyTable)
        dfDailyTable = self.cleanDailyDistributor(dfDailyTable)
        dfDailyTable = self.cleanDate(dfDailyTable)

    def runYear(self, year):
        # print(result)
        XPATH_Year = "//*[@class='a-link-normal' and text() = '{year}']".format(year=year)
        try:
            yearListDriver = driver.find_element(By.XPATH, XPATH_Year)
        except:
            WebDriverWait(driver, waitTime).until(EC.presence_of_element_located((By.XPATH, XPATH_Year)))
            yearListDriver = driver.find_element(By.XPATH, XPATH_Year)
        yearListDriver.click()
        self.clickFilters()
        rowNumber, colNumber = self.getRowColumnNumber()

        global dfYearlyTable
        dfYearlyTable = self.getTableData()
        self.cleanYearlyTable()

        print(dfYearlyTable)
        sheetName = self.sheetNameYear.format(year=year)
        self.writetoExcel(dfYearlyTable, sheetName)
        self.getAllDailyData(rowNumber)
        driver.execute_script("window.history.go(-1)")

    def run(self):
        for year in self.yearList:
            try:
                driver.get(urlYearly)
            except:
                print("Cannot access {url}...quitting now").format(url=urlYearly)
            self.runYear(year)
            sleep(self.sleepTime)
        self.cleanDailyTable()
        print(dfDailyTable)
        self.writetoExcel(dfDailyTable, self.sheetNameDaily)
        del wb['Sheet']
        wb.save(filename=self.totalFileName)
