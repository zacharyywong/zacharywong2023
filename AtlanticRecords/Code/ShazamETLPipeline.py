#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This program surfaces the most important songs of the day for Atlantic Records. 
# Author: Zachary Wong
# 1/16/2022

#import data libraries
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
driver = webdriver.Chrome(service = service)

# import libs, authorize gspread  
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = [
   'https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
google_key_file = '/Users/zacharywong/Documents/ServiceAccountKey-Secret/pelagic-tracker-338302-42be4f3c9805.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

#import email libs
import email, ssl, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase

# relative path to dataframe folder
pathtoDFolder = '/Users/zacharywong/github/zacharywong2023/AtlanticRecords/IntermediateDataFrames/'

# keep track of day/time 
est = pytz.timezone('US/Eastern')
fmt = '%d/%m/%Y %H:%M:%S'
now = datetime.now()
now = now.astimezone(est).strftime(fmt)
print("day/time: " + now)


# In[2]:


# Helper function: reads in values from Top 5 Important Songs Google Sheets
# Need spreadsheet ID and the cell address where the value should be read in 
# returns the value 

def readinValue(spreadsheet_id, cellLocation):
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.get_worksheet(0)
    value = worksheet.acell(cellLocation).value
    return value


# In[3]:


# Helper function: changes the cell value in the Top 5 Important Songs Google Sheets
# Need spreadsheet ID, the cell address where the value should in, and the value to read in 

def changeCellValue(spreadsheet_id, cellLocation, value):
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.get_worksheet(0)
    worksheet.update(cellLocation, value)


# In[4]:


# Grab and store variables for the rest of the code 
# SongLimit: top n number of songs to be read from both national and city charts
# Max Song Limit is 45: Shazam only has data for 45 songs for the WoonSocket, Rhode Island Top50 chart eventhough Shazam has data for all 50 songs for all other cities
# UnrankedSongChangedWeight: the increase/decrease in weight given to songs with rankings greater than SongLimit  

spreadsheet_id = '1WYvfPFW6n2hOCZ-2_pTT0hjJOj5vGHbwjLnjzDqXhSM'

# read in SongLimit value
# If user inputs songlimit more than 50, change it to 50 
cellLocationLimit = 'B10'
SongLimit = int(readinValue(spreadsheet_id, cellLocationLimit))
maxSongLimit = 50
if SongLimit > maxSongLimit: 
    SongLimit = maxSongLimit
    changeCellValue(spreadsheet_id, cellLocationLimit, maxSongLimit)

# read in unrankedSongChangedWeight
# if user inputs weight equal or less than 0, change weight to 1 
cellLocationWeight = 'B11'
UnrankedSongChangedWeight = int(readinValue(spreadsheet_id, cellLocationWeight))
minSongWeight = 1
if UnrankedSongChangedWeight < minSongWeight: 
    UnrankedSongChangedWeight = minSongWeight
    changeCellValue(spreadsheet_id, cellLocationWeight, minSongWeight)
    
print("SongLimit: "+ str(SongLimit) + ' ' + "UnrankedSongChangedWeight: " + str(UnrankedSongChangedWeight))


# In[5]:


# Scrape Shazam to fill in dataframe for US Top Charts
url = 'https://www.shazam.com/charts/top-200/united-states'
xpath = '//div[@class="download-csv"]/a'
filename = 'USTopSongs.csv'
path = pathtoDFolder + 'USTopSongs.csv'
driver.get(url)
waittime = 20

# Wait until web element is loaded
element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, xpath)))
csvlink = ''

# handles StaleElementReferenceException
try: 
    csv = driver.find_element(By.XPATH, xpath)
    csvlink = csv.get_attribute('href')


except: 
    csv = driver.find_element(By.XPATH, xpath)
    csvlink = csv.get_attribute('href')

# read in csv link, set up dataframe based on SongLimit, and export 
df = pd.read_csv(csvlink, skiprows=2)
columns = df.columns.tolist()
columns = columns[1:3] + columns[0:1]
dfUSTopSongs = df[columns].rename(columns={'Rank':'Rank in Top US Chart', 'Title': 'Song Name'}).head(SongLimit)
dfUSTopSongs.to_csv(path, index=False)
dfUSTopSongs.head()


# In[6]:


# Create a dictionary of cities and their csv links from Shazam 
xpath = '//select[@data-shz-type="city"]'
driver.get(url)
firstindex = 0
baseurl = 'https://www.shazam.com/services/charts/csv/top-50/united-states/'
driver.get(url)
element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, xpath)))
try:
    cities = driver.find_element(By.XPATH, xpath)
    dropdown = Select(cities)
    
except:
    cities = driver.find_element(By.XPATH, xpath)
    dropdown = Select(cities)

# Create a list of all cities with Top 50 Charts in dropdown menu on Shazam website
citylist = []
for city in dropdown.options:
    citynormalized = city.text.replace(',', '').replace(' ', '-')
    citylist.append(citynormalized)
citylist.pop(firstindex)

# remove Woonsocket, Rhode Island: number of songs in the Top 50 chart seems to vary (dropped from 45 to 40 songs in a day)
citylist.remove('Woonsocket')

#get csv links for each city and add city: url pairs to dictionary 
cityURL = {}
for city in citylist:
    csvurl = baseurl + str(city)
    cityURL[city] = csvurl
cityURL
driver.quit()
    


# In[7]:


#Create Panda Dataframe for each city 
columnsPart = ["Song Name", "Artist"]
columns = columnsPart + citylist
dfCityTopSongs = pd.DataFrame(columns = columns)
dfCityTopSongs


# In[8]:


# A Helper Function to fill in Song Rankings in the dfCityTopSongs dataframe 

def updateSongRank(dfCity, SongIndex, dfCityTopSongs, SongLimit, CityName):
    
    #Append top songs to the CityTop20 Dataframe 
    SongRank = 0
    while SongRank < SongLimit: 
        SongName =  dfCity.at[SongRank, 'Title']
        SongArtist =  dfCity.at[SongRank, 'Artist']
        
        # append new song/artist to dataframe if not already inside 
        if SongName not in dfCityTopSongs['Song Name'].unique():
            dfCityTopSongs = dfCityTopSongs.append({"Song Name": SongName, "Artist": SongArtist}, ignore_index = True)
            global SongIndexCounter
            SongIndex.update({SongName: SongIndexCounter})  
            SongIndexCounter += 1
            #print(SongName)
            
        # fill in the value (rank) for the song for the specific city if not the same as previous day
        # update rank for next song
        if (dfCityTopSongs.at[SongIndex.get(SongName), CityName] != SongRank+1):
            dfCityTopSongs.at[SongIndex.get(SongName), CityName] = SongRank+1
        SongRank += 1
    return dfCityTopSongs


# In[9]:


# Fill in the dfCityTopSongs dataframe for the rankings of each Top50 song for each city 

# Keeps track of the song and its index in the dfCityTopSongs dataframe 
SongIndex = {}
SongIndexCounter = 0
filename = 'CityTopSongs.csv'
path = pathtoDFolder + filename

# Loop through each city 
# Call updateSongRank helper function to add in rankings
# export to csv 
for cityName in citylist: 
    cityurl = cityURL.get(cityName)
    dfCity = pd.read_csv(cityurl, skiprows = 2)
    dfCityTopSongs = updateSongRank(dfCity, SongIndex, dfCityTopSongs, SongLimit, cityName)
dfCityTopSongs.to_csv(path, index = False)


# In[10]:


# Set indexes on the US and City dataframe to Song Name and Artist 

dfCityTopSongs = dfCityTopSongs.set_index(['Song Name', 'Artist'])
dfUSTopSongs = dfUSTopSongs.set_index(['Song Name', 'Artist'])
dfUSTopSongs.head()


# In[11]:


# Calculate the Importance Score for each Song
# 1. add up all rankings in each city (songs that didn't break into a city top chart is the number of cities + UnrankedSongChangedWeight)
# 2. Divide by number of cities 
# 3. Thus, most important songs have lowest Importance Score 

NumberofCities = len(citylist)
NonRankedWeight = SongLimit + UnrankedSongChangedWeight
dfCityTopSongs['Sum of Rankings'] = dfCityTopSongs.sum(axis = 1)
dfCityTopSongs['Number of Cities without Rank'] = dfCityTopSongs.isna().sum(axis = 1)

# Importance Calculation applied to each row
def calculateImportance(row):
    row['Importance Score'] = (row['Sum of Rankings'] + (row['Number of Cities without Rank'] * NonRankedWeight))/NumberofCities
    return row
dfCityTopSongs = dfCityTopSongs.apply(calculateImportance, axis = 'columns')
dfCityTopSongs['Importance Score'] = dfCityTopSongs['Importance Score'].round(2)

#Clean up dataframe 
del(dfCityTopSongs['Sum of Rankings'])
del(dfCityTopSongs['Number of Cities without Rank'])

dfCityTopSongs.head()


# In[12]:


# Add in column counting how many cities the song broke Top 20 Charts
ColumnName = 'Number of Cities where Song Broke Top Chart'
Series = dfCityTopSongs.count(axis = 'columns')-1
Series = Series.rename(ColumnName)
dfCityTopSongs = pd.concat([dfCityTopSongs, Series], axis = 1)
dfCityTopSongs.head()


# In[13]:


# Concatenate the US and city dataframes into 1 dataframe
df = pd.concat([dfUSTopSongs, dfCityTopSongs], axis=1)
df.head()


# In[14]:


# Add Another column that shows if the song broke US Top 20 Chart
# df['Broke US Top Chart'] = np.where(pd.isna(df['Rank in Top US Chart']), False, True) is more concise but slow- results in highly fragmented dataframe

df = df.reset_index()
ColumnName = 'Broke US Top Chart'
Series = pd.Series(np.where(pd.isna(df['Rank in Top US Chart']), False, True))
Series = Series.rename(ColumnName)
df = pd.concat([df, Series], axis = 1)
df = df.set_index(['Song Name', 'Artist'])
df.head()


# In[15]:


# Reorder columns and export merged dataframe as csv

filename = 'TopSongsinUSandCity.csv'
path = pathtoDFolder + filename
columns = df.columns.tolist()
columns = columns[0:1] + columns[-3:] + columns[1:]
del columns[-3:]
df = df[columns]

TempImportanceScore = df['Importance Score']
df = df.drop(columns=['Importance Score'])
df.insert(loc=0, column='Importance Score', value=TempImportanceScore)

#Reorder columns and export final, merged dataframe as CSV
df = df.reset_index()
df = df.set_index('Importance Score').sort_index(axis = 0, ascending = True)
df.to_csv(path)


# In[16]:


# Create a new dataframe with only important songs (songs in this dataframe that has not broken the US Top Chart yet)
# Important Songs are songs that have broken into at least one city's Top Chart but has not broken into the US Top Chart
# delete the column 'Rank in USTop20 Chart

filename = 'MostImportantSongsinUS.csv'
path = pathtoDFolder + filename

important_df = df[(df['Number of Cities where Song Broke Top Chart']>0) & (df['Broke US Top Chart'] == False)]
important_df = important_df.reset_index()
important_df = (important_df
                    .set_index(['Importance Score'])
                    .sort_index(axis = 0, ascending = True))
important_df = important_df.drop(columns = ['Rank in Top US Chart'])

#Export to CSV 
important_df.to_csv(path)


# In[17]:


# Create another column in dataframe that lists all the cities that each song broke into its top charts

#Set index to Song name and artist and keep only columns of cities in new dataframe 
df = important_df.reset_index()
df = df.set_index(['Song Name', 'Artist']).head()
df_new = df.loc[:, 'Aberdeen-SD':'Yuma']

# Rotate columns and axis to make the songs/artists keys in the dictionary 
df_new = df_new.T

# Total dataframe in dictionary form 
# keys = song/artist tuple 
# Value = dictionary where key = column name and value = element from dataframe
dict = df_new.to_dict()
dict

#Populate a new dictionary where its keys = songs/artist and values = all cities that the song is in its top20 chart
SongCitiesDict = {}
ColumnName = 'List of Cities where Song Broke Top Chart'

# Extract song/artist name 
for Song in dict:
    CityList = []
    CityDict = dict.get(Song)
    for City in CityDict:
        if pd.isna(CityDict.get(City)) == False:
            CityList.append(City)
    SongCitiesDict[Song] = CityList
    
    #Turn CityList into a string to insert into the original df dataframe 
    CityList = ', '.join([str(city) for city in CityList])
    df.loc[Song, ColumnName] = CityList
df.head()


# In[18]:


#Reorder Columns
columns = df.columns.tolist()
columns = columns[0:2]+ columns[-1:] + columns[2:]
del columns[-1:]
df = df[columns]
df


# In[19]:


# CSV deliverable exported to CSV 
path = '/Users/zacharywong/github/zacharywong2023/AtlanticRecords/Top5ImportantSongs.csv'
df = df.reset_index()
df.to_csv(path, index = False)


# In[20]:


# Update Google Spreadsheet 

df = df.fillna('')
spreadsheet_id = '1WYvfPFW6n2hOCZ-2_pTT0hjJOj5vGHbwjLnjzDqXhSM'
spreadsheet_name = 'Top 5 Important Songs of the Day'
sh = gc.open_by_key(spreadsheet_id)
worksheet = sh.get_worksheet(0)
worksheet.update([df.columns.values.tolist()] + df.values.tolist())


# In[21]:


# Send email with deliverable file attached if user chooses not to pause emails

# read in value for paused email
PauseEmailCellLocation = 'B12'
EmailPause = readinValue(spreadsheet_id, PauseEmailCellLocation)

#If not paused, send email
if (EmailPause == 'N'):
    
    # assign emails, passwords, and csv file to variables
    subject = 'Top 5 Most Important Songs of the Day'
    text = "Hi Jake and the team, \n\nAttached is today's CSV attachment with the Top 5 Most Important Songs of the Day you should look out for! \nFor your convenience, here is the link to the auto-generated Google Spreadsheet with dynamic tables/graphs: \nhttps://docs.google.com/spreadsheets/d/1WYvfPFW6n2hOCZ-2_pTT0hjJOj5vGHbwjLnjzDqXhSM/edit?usp=sharing \n\nBest Regards, \nZachary Wong"
    sender_email = "zacharywongdatascience"
    receiver_email = 'jake.stern@atlanticrecords.com'
    password = ''
    pathtoPassword = '/Users/zacharywong/Documents/ApplicationPassword-Secret/ApplicationPassword.txt'
    with open (pathtoPassword, 'r') as file:
        password = file.read()
    filename = 'Top5ImportantSongs-' + str(date.today()) +'.csv'
    filepath = '/Users/zacharywong/github/zacharywong2023/AtlanticRecords/Top5ImportantSongs.csv'

    # Attach each component with respective MIMEMultipart 
    msg = MIMEMultipart()
    msg ["From"] = sender_email
    msg ["To"] = receiver_email
    msg ["Subject"] = subject
    msg.attach(MIMEText(text, "plain"))
    with open (filepath, 'rb') as file:
        msg.attach(MIMEApplication(file.read(), Name=filename))
    
    # attach file metadata
    msg['Content Disposition'] = "attachment; filename=Top5ImportantSongs"
    
    # send email through SSL 
    content = msg.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, content)


# In[ ]:




