from random import random
import math
import random

from dateutil.relativedelta import relativedelta
from openpyxl import Workbook
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from time import sleep
import pytz
from openpyxl.utils.dataframe import dataframe_to_rows

# import selenium/webscraping libs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class WebScrape:

    def __init__(self, waitTime, sleepTime1, sleepTime2):

        self.sleepTime1 = sleepTime1
        self.sleepTime2 = sleepTime2
        self.waitTime = waitTime

    def genSleep(self):
        sleepTime = random.randrange(self.sleepTime1, self.sleepTime2)
        print("sleepTime: " + str(sleepTime))
        return sleepTime


    # returns updated driver and retrieved element by XPATH
    def getElementXPATH(self, driver, XPATH):
        try:
            element = driver.find_element(By.XPATH, XPATH)
        except:
            WebDriverWait(driver, self.waitTime).until(EC.presence_of_element_located((By.XPATH, XPATH)))
            element = driver.find_element(By.XPATH, XPATH)
        return driver, element

    # returns updated driver and retrieved list of elements by XPATH
    def getElementsClass(self, driver, className):
        # //*[@id="table"]/div/table[2]/tbody/tr[2]/td[2]/a
        try:
            list = driver.find_elements(By.CLASS_NAME, className)
        except:
            WebDriverWait(driver, self.waitTime).until(EC.presence_of_element_located((By.CLASS_NAME, className)))
            list = driver.find_elements(By.CLASS_NAME, className)
        return driver, list

