#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This program builds an ETL pipeline using Shazam data collected through an API to surface the most important songs of the day 
# Sends an automated email and auto-updates a Google Spreadsheet with results/dynamic graphs 
# Author: Zachary Wong
# 1/16/2022

#import data libraries
import pandas as pd
import numpy as np
from datetime import date, datetime
import pytz 
import requests 

# import libs, authorize gspread  
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = [
   'https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
google_key_file = '/Users/zacharywong/Documents/ServiceAccountKey-Secret/pelagic-tracker-338302-eaf0e0e671cb.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

APIkey = ''
pathtoKey = '/Users/zacharywong/Documents/RapidAPIShazamKey/RapidAPIKey.txt'
with open (pathtoKey, 'r') as file:
    APIKey = file.read()

#import email libs
import email, ssl, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase

# relative path to dataframe folder
pathtoDFolder = '/Users/zacharywong/github/zacharywong2023/ShazamETLPipeline/IntermediateDataFrames/'

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
# Max Song Limit is 50 because each city has a Top 50 song chart. 
# UnrankedSongChangedWeight: the increase/decrease in weight given to songs with rankings greater than SongLimit  

spreadsheet_id = '1WYvfPFW6n2hOCZ-2_pTT0hjJOj5vGHbwjLnjzDqXhSM'

# read in SongLimit value
# If user inputs songlimit more than 50, change it to 50 
cellLocationLimit = 'B10'
SongLimit = int(readinValue(spreadsheet_id, cellLocationLimit))
maxSongLimit = 20
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


#Create two data frames that will be merged later 

dfUSTop20 = pd.DataFrame(columns=["Song Name","Artist","Rank in USTop20 Chart"])
dfCityTop20 = pd.DataFrame(columns=["Song Name","Artist"])
dfCityTop20

#Call API For list of countries and its cities

USCitiesURL= "https://shazam-core.p.rapidapi.com/v1/frame/cities"

headers = {
    'x-rapidapi-host': "shazam-core.p.rapidapi.com",
    'x-rapidapi-key': APIKey
    }

USCitiesResponse = requests.request("GET", USCitiesURL, headers = headers).json()

#Extract all cities from the US and put each list containing CityID, CityName into a list 
USCities = []
CityIndex = 0
NumberofCities = 202
while CityIndex != NumberofCities:
    CityIDName = []
    CityIDName.append(USCitiesResponse[9]['cities'][CityIndex]['id'])
    CityIDName.append(USCitiesResponse[9]['cities'][CityIndex]['name'])
    USCities.append(CityIDName)
    CityIndex = CityIndex + 1

USCities[0:5]


# In[6]:


# A Helper Function to fill in Song Rankings in the dfCityTop20 dataframe 

def updateSongRank(SongListResponse, SongIndex, dfCityTop20, SongLimit):
    
    #Append top 20 songs to the CityTop20 Dataframe 
    SongRank = 0
    while SongRank < SongLimit: 
        SongName = SongListResponse[SongRank]['title']
        SongArtist = SongListResponse[SongRank]['subtitle']
        
        # append new song/artist to dataframe if not already inside 
        if SongName not in dfCityTop20['Song Name'].unique():
            dfCityTop20 = dfCityTop20.append({"Song Name": SongName, "Artist": SongArtist}, ignore_index = True)
            global SongIndexCounter
            SongIndex.update({SongName: SongIndexCounter})  
            SongIndexCounter += 1
            #print(SongName)
            
        # fill in the value (rank) for the song for the specific city if not the same as previous day
        # update rank for next song
        if (dfCityTop20.at[SongIndex.get(SongName), CityName] != SongRank+1):
            dfCityTop20.at[SongIndex.get(SongName), CityName] = SongRank+1
        SongRank += 1
        
    #print(SongIndex)
    #Reset song rank
    return dfCityTop20


# In[7]:


# API Call for Top20 Songs for first 20 cities 
CityChartURL = "https://shazam-core.p.rapidapi.com/v1/charts/city"

headers = {
    'x-rapidapi-host': "shazam-core.p.rapidapi.com",
    'x-rapidapi-key': APIKey
    }

maxCityLimit = 20
for CityIndex in range(0, maxCityLimit):
    dfCityTop20[USCities[CityIndex][1]] = None 
    
dfCityTop20

# Fill in the CityTop20 Dataframe for first 20 cities in the list 
# Only use first 20 cities to limit the number of API Calls for this assignment 

SongLimit = 20
CityIndex = 0

# Keeps track of the song and its index in the dfCityTop20 dataframe 
SongIndex = {}
SongIndexCounter = 0

# Loop through each city 
for CityIndex in range(0, 20): 
    
    # extract the cityID and City Name for this city
    CityID = USCities[CityIndex][0]
    CityName = USCities[CityIndex][1]
        
    # API Call to get the top20 Shazam Chart for the city and call helper function to fill in song rankings  
    querystring = {"city_id":CityID,"limit": SongLimit}
    SongListResponse= requests.request("GET", CityChartURL, headers=headers, params=querystring).json()
    dfCityTop20 = updateSongRank(SongListResponse, SongIndex, dfCityTop20, SongLimit)
    
    #update City Index 
    CityIndex = CityIndex + 1

dfCityTop20


# In[8]:


#Call for the Top20 Songs from the US Chart

USChartURL = "https://shazam-core.p.rapidapi.com/v1/charts/country"

querystring = {"country_code":"US","limit":"50"}

headers = {
    'x-rapidapi-host': "shazam-core.p.rapidapi.com",
    'x-rapidapi-key': APIKey
    }

USChartResponse = requests.request("GET", USChartURL, headers=headers, params=querystring).json()

#USChartResponse

# Fill in the USTop20 Datframe with song/artist/ranking 

SongIndex = 0
while(SongIndex < 20):
    SongName = USChartResponse[SongIndex]['title']
    SongArtist = USChartResponse[SongIndex]['subtitle']
    #print(SongName, SongArtist, SongIndex)
    dfUSTop20 = dfUSTop20.append({"Song Name": SongName, "Artist": SongArtist, "Rank in Top US Chart": SongIndex+1}, ignore_index=True)
    SongIndex += 1

dfUSTop20


# In[9]:


# Set indexes on the US and City dataframe to Song Name and Artist 

dfCityTopSongs = dfCityTop20.set_index(['Song Name', 'Artist'])
dfUSTopSongs = dfUSTop20.set_index(['Song Name', 'Artist'])
dfUSTop20.head()


# In[10]:


# Calculate the Importance Score for each Song
# 1. add up all rankings in each city (songs that didn't break into a city top chart is the number of cities + UnrankedSongChangedWeight)
# 2. Divide by number of cities 
# 3. Thus, most important songs have lowest Importance Score 

NumberofCities = maxCityLimit
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


# In[11]:


# Add in column counting how many cities the song broke Top 20 Charts
ColumnName = 'Number of Cities where Song Broke Top Chart'
Series = dfCityTopSongs.count(axis = 'columns')-1
Series = Series.rename(ColumnName)
dfCityTopSongs = pd.concat([dfCityTopSongs, Series], axis = 1)
dfCityTopSongs.head()


# In[12]:


# Concatenate the US and city dataframes into 1 dataframe
df = pd.concat([dfUSTopSongs, dfCityTopSongs], axis=1)
df.head()


# In[13]:


# Add Another column that shows if the song broke US Top 20 Chart
# df['Broke US Top Chart'] = np.where(pd.isna(df['Rank in Top US Chart']), False, True) is more concise but slow- results in highly fragmented dataframe

df = df.reset_index()
ColumnName = 'Broke US Top Chart'
Series = pd.Series(np.where(pd.isna(df['Rank in Top US Chart']), False, True))
Series = Series.rename(ColumnName)
df = pd.concat([df, Series], axis = 1)
df = df.set_index(['Song Name', 'Artist'])
df.head()


# In[14]:


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


# In[15]:


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


# In[16]:


# Create another column in dataframe that lists all the cities that each song broke into its top charts

#Set index to Song name and artist and keep only columns of cities in new dataframe 
df = important_df.reset_index()
df = df.set_index(['Song Name', 'Artist']).head()
df_new = df.loc[:, 'New York City':'Orlando']

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


# In[17]:


#Reorder Columns
columns = df.columns.tolist()
columns = columns[0:2]+ columns[-1:] + columns[2:]
del columns[-1:]
df = df[columns]
df


# In[18]:


# CSV deliverable exported to CSV 
path = '/Users/zacharywong/github/zacharywong2023/ShazamETLPipeline/Top5ImportantSongs.csv'
df = df.reset_index()
df.to_csv(path, index = False)


# In[19]:


# Update Google Spreadsheet 

df = df.fillna('')
spreadsheet_id = '1WYvfPFW6n2hOCZ-2_pTT0hjJOj5vGHbwjLnjzDqXhSM'
spreadsheet_name = 'Top 5 Important Songs of the Day'
sh = gc.open_by_key(spreadsheet_id)
worksheet = sh.get_worksheet(0)
worksheet.update([df.columns.values.tolist()] + df.values.tolist())


# In[20]:


# Send email with deliverable file attached if user chooses not to pause emails

# read in value for paused email
PauseEmailCellLocation = 'B12'
EmailPause = readinValue(spreadsheet_id, PauseEmailCellLocation)

#If not paused, send email
if (EmailPause == 'N'):
    
    # assign emails, passwords, and csv file to variables
    subject = 'Top 5 Most Important Songs of the Day'
    text = "Hi, \n\nAttached is today's CSV attachment with the Top 5 Most Important Songs of the Day you should look out for! \nFor your convenience, here is the link to the auto-generated Google Spreadsheet with dynamic tables/graphs: \nhttps://docs.google.com/spreadsheets/d/1WYvfPFW6n2hOCZ-2_pTT0hjJOj5vGHbwjLnjzDqXhSM/edit?usp=sharing \n\nBest Regards, \nZachary Wong"
    sender_email = "zacharywongdatascience"
    receiver_email = 'zachary.j.wong.23@dartmouth.edu'
    password = ''
    pathtoPassword = '/Users/zacharywong/Documents/ApplicationPassword-Secret/ApplicationPassword.txt'
    with open (pathtoPassword, 'r') as file:
        password = file.read()
    filename = 'Top5ImportantSongs-' + str(date.today()) +'.csv'
    filepath = '/Users/zacharywong/github/zacharywong2023/ShazamETLPipeline/Top5ImportantSongs.csv'

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




