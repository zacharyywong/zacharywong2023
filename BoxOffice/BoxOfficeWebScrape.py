# Box Office Mojo - daily data on top wide releases yearly in 2021 and 2022

# import data libraries
import pandas as pd
import numpy as np
from datetime import date, datetime
import pytz

# import selenium/webscraping libs
from urllib.request import urlopen
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Access webdriver for Chrome
driver_path = '/Users/zacharywong/Downloads/chromedriver'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# keep track of day/time
est = pytz.timezone('US/Eastern')
fmt = '%d/%m/%Y %H:%M:%S'
now = datetime.now()
now = now.astimezone(est).strftime(fmt)
print("day/time: " + now)

urlYearly = 'https://www.boxofficemojo.com/year/?ref_=bo_nb_hm_secondarytab'


def run():
    driver.get(urlYearly)
    driver.find_element(By.XPATH, "//*[@id='table']/div/table[2]/tbody/tr[2]/td[1] and text() = '2022'")
    driver.click()
if __name__ == '__main__':
    run()
