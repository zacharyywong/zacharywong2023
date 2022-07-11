import subprocess
import sys

from openpyxl import Workbook
import pandas as pd
import numpy as np
from datetime import datetime
from time import sleep
import pytz
import random
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
sleepTime = random.randrange(4, 7)

# keep track of day/time
est = pytz.timezone('US/Eastern')
fmt = '%d/%m/%Y %H:%M:%S'
now = datetime.now()
now = now.astimezone(est).strftime(fmt)
print("day/time: " + now)

# excel
path = "/Users/zacharywong/github/zacharywong2023/BoxOffice/"
totalFileName = "DecayCurveData-{date}.xlsx".format(date = now)
wb = Workbook()

urlYearly = 'https://www.boxofficemojo.com/year/?ref_=bo_nb_hm_secondarytab'
dailyColumns = ["Date", "DOW", "Rank", "Daily", "%+/-YR", "%+/-LW", "Theaters", "Avg", "To Date", "Day", "Title",
                "Genre", "Distributor"]
yearlyColumns = ["Rank", "Release", "Gross", "Max Th", "Opening", "% of Total", "Open Th", "Open", "Close",
                 "Distributor"]

dfDailyTable = pd.DataFrame()
dfYearlyTable = pd.DataFrame()

yearList = [2022, 2021]

class BoxOfficeWebScrape:

    def __init__(self, urlYearly):
        self.urlYearly = urlYearly

    def writetoExcel(self, df, sheetName):
        ws = wb.create_sheet()
        ws.title = sheetName
        rows = dataframe_to_rows(df, index=False, header=True)
        for row in rows:
            ws.append(row)
        wb.save(filename=totalFileName)

    # Filter by In Year Releases and Wide Releases
    def clickFilters(self):
        XPATHinYear = "/html/body/div[1]/main/div/div/div[1]/div[2]/span/form/span/select"
        XPATHwideRelease = "/html/body/div[1]/main/div/div/div[1]/div[3]/span/form/span/select"
        sleep(sleepTime)

        try:
            filterInYearSelect = Select(driver.find_element(By.XPATH, XPATHinYear))
        except:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATHinYear)))
            filterInYearSelect = Select(driver.find_element(By.XPATH, XPATHinYear))

        filterInYearSelect.select_by_visible_text("In-year releases")
        sleep(sleepTime)

        try:
            filterwidereleaseSelect = Select(driver.find_element(By.XPATH, XPATHwideRelease))
        except:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATHwideRelease)))
            filterwidereleaseSelect = Select(driver.find_element(By.XPATH, XPATHwideRelease))

        filterwidereleaseSelect.select_by_visible_text("Wide releases")

    def getMovieLink(self, index):
        # //*[@id="table"]/div/table[2]/tbody/tr[2]/td[2]/a
        XPATHMovie = "//*[@id='table']/div/table[2]/tbody/tr[{index}]/td[2]/a".format(index=index)
        try:
            movie = driver.find_element(By.XPATH, XPATHMovie)
        except:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATHMovie)))
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

    def cleanTable(self, df):
        for column in df:
            df[column] = df[column].replace(['-'], np.nan)
            # if df[column].dtypes == bool:
            #    df.drop(column, inplace = True, axis = 1)
        df = df.dropna(axis=1, how='all')
        df = df.drop(df.columns[[10]], axis=1)
        return df

    def renameYearlyTable(self, df):
        df.columns = yearlyColumns
        return df

    def renameDailyTable(self, df):
        df.columns = dailyColumns
        return df

    def reorderDailyTable(self, df):
        colsOrdered = ["Distributor", "Title", "Genre", "Date", "DOW", "Rank", "Daily", "%+/-YR", "%+/-LW", "Theaters",
                       "Avg", "To Date", "Day"]
        df = df[colsOrdered]
        return df

    def cleanDailyDistributor(self, df):
        df["Distributor"] = df["Distributor"].str.split('\n').str[0]
        return df

    def cleanDate(self, df):
        df["Date"] = df["Date"].str.split('COVID-19 Pandemic').str[0]
        return df

    def getDailyMovieData(self, movieTitle):
        rowNumber, colNumber = self.getRowColumnNumber()
        indexList = []
        XPATHGenre = "//*[@id='a-page']/main/div/div[3]/div[4]/div[6]/span[2]"
        XPATHDistributor = "//*[@id='a-page']/main/div/div[3]/div[4]/div[1]/span[2]"
        #            value = (driver.find_element(By.XPATH, XPATHValue)).text
        for number in range(0, rowNumber):
            indexList.append(number)

        #tempResult = pd.DataFrame(index=indexList)
        tempResult = self.getTableData()
        tempResult["Title"] = movieTitle
        tempResult["Genre"] = (driver.find_element(By.XPATH, XPATHGenre)).text
        tempResult["Distributor"] = (driver.find_element(By.XPATH, XPATHDistributor)).text
        return tempResult

    def getAllDailyData(self, rowNumber):
        print("Number of Movies:" + str(rowNumber))
        index = 40
        while index < rowNumber + 2:
            print("index: " + str(index))
            startNow = datetime.now()
            movieDriver, movieTitle = self.getMovieLink(index)
            print(movieTitle)
            movieDriver.click()
            self.getRowColumnNumber()
            try:
                tempResult = self.getDailyMovieData(movieTitle)
            except:
                print("cannot read movies further - most likely website overload")
            global dfDailyTable
            dfDailyTable = pd.concat([dfDailyTable, tempResult])
            index += 1

            sleep(sleepTime)
            driver.execute_script("window.history.go(-1)")
            sleep(sleepTime)
            endNow = datetime.now()
            timeElapsed = endNow - startNow
            print("time elapsed: " + str(timeElapsed))

    def runYear(self, year, sheetName):
        # print(result)
        XPATH_Year = "//*[@class='a-link-normal' and text() = '{year}']".format(year=year)
        try:
            yearListDriver = driver.find_element(By.XPATH, XPATH_Year)
        except:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATH_Year)))
            yearListDriver = driver.find_element(By.XPATH, XPATH_Year)
        yearListDriver.click()
        self.clickFilters()
        rowNumber, colNumber = self.getRowColumnNumber()

        global dfYearlyTable
        dfYearlyTable = self.getTableData()
        dfYearlyTable = self.cleanTable(dfYearlyTable)
        dfYearlyTable = self.renameYearlyTable(dfYearlyTable)
        sheetName = sheetName.format(year = year)
        print(dfYearlyTable)
        self.writetoExcel(dfYearlyTable, sheetName)
        self.getAllDailyData(rowNumber)
        driver.execute_script("window.history.go(-1)")
