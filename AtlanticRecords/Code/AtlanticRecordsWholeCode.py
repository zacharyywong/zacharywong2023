#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from datetime import date


from urllib.request import urlopen
import requests 
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

driver_path = '/Users/zacharywong/Downloads/chromedriver'
service = Service(driver_path)
driver = webdriver.Chrome(service = service)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
   'https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
google_key_file = '/Users/zacharywong/Documents/ServiceAccountKey-Secret/pelagic-tracker-338302-42be4f3c9805.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

#from email import encoders
import email, ssl, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase

from datetime import date

#relative path to dataframe folder
pathtoDFolder = '../IntermediateDataFrames/'


# In[ ]:


def readinValue(spreadsheet_id, cellLocation):
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.get_worksheet(0)
    value = worksheet.acell(cellLocation).value
    return int(value)


# In[ ]:


spreadsheet_id = '1WYvfPFW6n2hOCZ-2_pTT0hjJOj5vGHbwjLnjzDqXhSM'
cellLocationLimit = 'B9'
cellLocationWeight = 'B10'
SongLimit = readinValue(spreadsheet_id, cellLocationLimit)
UnrankedSongChangedWeight = readinValue(spreadsheet_id, cellLocationWeight)
SongLimit
UnrankedSongChangedWeight


# In[ ]:


url = 'https://www.shazam.com/charts/top-200/united-states'
xpath = '//div[@class="download-csv"]/a'
filename = 'USTopSongs.csv'
path = pathtoDFolder + 'USTopSongs.csv'
driver.get(url)
waittime = 20
element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, xpath)))
csvlink = ''

try: 
    csv = driver.find_element(By.XPATH, xpath)
    csvlink = csv.get_attribute('href')


except: 
    csv = driver.find_element(By.XPATH, xpath)
    csvlink = csv.get_attribute('href')

df = pd.read_csv(csvlink, skiprows=2)
columns = df.columns.tolist()
columns = columns[1:3] + columns[0:1]
dfUSTopSongs = df[columns].rename(columns={'Rank':'Rank in Top US Chart', 'Title': 'Song Name'}).head(SongLimit)
dfUSTopSongs.to_csv(path, index=False)
dfUSTopSongs


# In[ ]:


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

#cities
citylist = []

for city in dropdown.options:
    citynormalized = city.text.replace(',', '').replace(' ', '-')
    citylist.append(citynormalized)
citylist.pop(firstindex)
len(citylist)

#get csv links for each city in dictionary 

cityURL = {}
for city in citylist:
    csvurl = baseurl + str(city)
    cityURL[city] = csvurl

cityURL
driver.quit()
    


# In[ ]:


#Create Panda Dataframe
columnsPart = ["Song Name", "Artist"]
columns = columnsPart + citylist
dfCityTopSongs = pd.DataFrame(columns = columns)
dfCityTopSongs


# In[ ]:


# A Helper Function to fill in Song Rankings in the dfCityTopSongs dataframe 

def updateSongRank(dfCity, SongIndex, dfCityTopSongs, SongLimit, CityName):
    
    #Append top 20 songs to the CityTop20 Dataframe 
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
        
    #print(SongIndex)
    #Reset song rank
    return dfCityTopSongs


# In[ ]:


# Keeps track of the song and its index in the dfCityTopSongs dataframe 
SongIndex = {}
SongIndexCounter = 0
filename = 'CityTopSongs.csv'
path = pathtoDFolder + filename

# Loop through each city 
for cityName in citylist: 
    cityurl = cityURL.get(cityName)
    dfCity = pd.read_csv(cityurl, skiprows = 2)
    dfCityTopSongs = updateSongRank(dfCity, SongIndex, dfCityTopSongs, SongLimit, cityName)

dfCityTopSongs.to_csv(path, index = False)


# In[ ]:


# Set indexes on the City Chart dataframe to Song Name and Artist 
# Set indexes on the USTop50 DataFrame to Song Name and Artist

dfCityTopSongs = dfCityTopSongs.set_index(['Song Name', 'Artist'])
dfUSTopSongs = dfUSTopSongs.set_index(['Song Name', 'Artist'])
dfUSTopSongs


# In[ ]:


# Importance Score Calculation
# 1. add up all rankings in each city (songs that didn't break into a city are all counted as 21 rank)
# 2. Divide by number of cities 
# 3. Thus, most important songs have lowest Importance Score 

NumberofCities = 202
NonRankedWeight = NumberofCities + UnrankedSongChangedWeight

dfCityTopSongs['Sum of Rankings'] = dfCityTopSongs.sum(axis = 1)
dfCityTopSongs['Number of Cities without Rank'] = dfCityTopSongs.isna().sum(axis = 1)
def calculateImportance(row):
    row['Importance Score'] = (row['Sum of Rankings'] + (row['Number of Cities without Rank'] * NonRankedWeight))/NumberofCities
    return row
dfCityTopSongs = dfCityTopSongs.apply(calculateImportance, axis = 'columns')

#Clean up dataframe 

del(dfCityTopSongs['Sum of Rankings'])
del(dfCityTopSongs['Number of Cities without Rank'])

dfCityTopSongs.head()


# In[ ]:


# Add in column counting how many cities the song broke Top 20 Charts
ColumnName = 'Number of Cities where Song Broke Top Chart'
dfCityTopSongs[ColumnName] = dfCityTopSongs.count(axis = 'columns')-1
dfCityTopSongs.head()


# In[ ]:


# Concatenate the two dataframes into 1 dataframe

df = pd.concat([dfUSTopSongs, dfCityTopSongs], axis=1)
df.head()


# In[ ]:


# Add Another column that shows if the song broke US Top 20 Chart

df['Broke US Top Chart'] = np.where(pd.isna(df['Rank in Top US Chart']), False, True)
df


# In[ ]:


filename = 'TopSongsinUSandCity.csv'
path = pathtoDFolder + filename

#Reorder columns

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


# In[ ]:


# Create a new dataframe with only important songs (songs in this dataframe that has not broken the USTop20 Chart yet)
# Important Songs are songs that have broken into at least one city's Top20 Charts but has not broken into the US Top20 Chart
# delete the column 'Rank in USTop20 Chart

filename = 'MostImportantSongsinUS.csv'
path = pathtoDFolder + filename

important_df = df[(df['Number of Cities where Song Broke Top Chart']>0) & (df['Broke US Top Chart'] == False)]
important_df = important_df.reset_index()
important_df = (important_df
                    .set_index(['Importance Score'])
                    .sort_index(axis = 0, ascending = True))
important_df = important_df.drop(columns = ['Rank in Top US Chart'])
important_df.head()

#Export to CSV 
important_df.to_csv(path)


# In[ ]:


df = important_df.reset_index()
df = df.set_index(['Song Name', 'Artist']).head()

#Set index to Song name and artist, keep only columns of cities, and extract top 5 Most Important Songs 
df_new = df.loc[:, 'Aberdeen-SD':'Yuma']
df_new


# In[ ]:


# Create a dictionary out of the dataframe to extract all cities that each song is in its Top20 Chart
# Rotate columns and axis to make the songs/artists keys in the dictionary 
df_new = df_new.T

# Total dataframe in dictionary form 
# keys = song/artist tuple 
# Value = dictionary where key = column name and value = element from dataframe
dict = df_new.to_dict()
dict


# In[ ]:


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
df
    


# In[ ]:


#Reorder Columns
columns = df.columns.tolist()
columns = columns[0:2]+ columns[-1:] + columns[2:]
del columns[-1:]
df = df[columns]
df


# In[ ]:


# Export to CSV
path = '/Users/zacharywong/github/zacharywong2023/AtlanticRecords/Deliverable-Top5ImportantSongs.csv'
df = df.reset_index()
df.to_csv(path, index = False)


# In[ ]:


df = df.fillna('')

spreadsheet_id = '1WYvfPFW6n2hOCZ-2_pTT0hjJOj5vGHbwjLnjzDqXhSM'
spreadsheet_name = 'Top 5 Important Songs of the Day'

sh = gc.open_by_key(spreadsheet_id)
worksheet = sh.get_worksheet(0)
worksheet.update([df.columns.values.tolist()] + df.values.tolist())


# In[ ]:


subject = 'Top 5 Most Important Songs of the Day'
text = 'Hi Jake and the team, here is a CSV attachment with the 5 most important songs of the day you should look out for.'
sender_email = "zacharywongdatascience"
receiver_email = 'zachary.j.wong.23@dartmouth.edu'
password = ''
pathtoPassword = '/Users/zacharywong/Documents/ApplicationPassword-Secret/ApplicationPassword.txt'
with open (pathtoPassword, 'r') as file:
    password = file.read()
filename = 'Top5ImportantSongs-' + str(date.today()) +'.csv'


# In[ ]:


filepath = '/Users/zacharywong/github/zacharywong2023/AtlanticRecords/Deliverable-Top5ImportantSongs.csv'

msg = MIMEMultipart()
msg ["From"] = sender_email
msg ["To"] = receiver_email
msg ["Subject"] = subject
msg.attach(MIMEText(text, "plain"))

with open (filepath, 'rb') as file:
    msg.attach(MIMEApplication(file.read(), Name=filename))

msg['Content Disposition'] = "attachment; filename=Top5ImportantSongs"
content = msg.as_string()

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, content)


# In[ ]:




