Project Write-Up:

Deliverables: This project's deliverables come in 2 forms and are updated/sent daily at a little past 12:00am EST with the top 5 most important songs of the day:

* "Top 5 Important Songs of the Day" Google Spreadsheet: An auto-generated spreadsheet that includes user input options to customize the Importance Score calculation and to pause/unpause daily emails. Link to the Google Sheet: https://docs.google.com/spreadsheets/d/1WYvfPFW6n2hOCZ-2_pTT0hjJOj5vGHbwjLnjzDqXhSM/edit?usp=sharing

* Daily Email: an email sent daily attached with the Top5ImportantSongs.csv file and the link to the Google Spreadsheet updated for that day (the sender email: zacharywongdatascience@gmail.com).

How To Read the Importance Scores:

* The most important songs are those that have broken into multiple cities’ Top Shazam Charts with high rankings but have not broken into Shazam’s national US Top Chart yet.

* The idea behind this definition of Importance is that it’s crucial for the recording label to know which songs/artists people are listening to in each city that have not caught onto national attention yet. If one of Atlantic Records’ artists has a song of high importance as per this definition, the recording label can invest in more resources to boost this song to more radio channels/streaming playlists for greater revenue. Atlantic Records can also use this data to sign new artists before they become bigger national hits: this program will help them identify up and coming talent.

* The Importance Score is calculated by first adding up all the rankings from each city's top chart for each song. If a song isn’t ranked in a particular city's top chart, its rank for that city is automatically calculated by adding the chart's lowest ranking number + an additional value that the user inputs through the Google Sheet called the Unranked Song Score (user input further explained below). This total sum is finally divided by the number of cities. Adding the Unranked Song Score increases the Importance Score for songs that do not rank in the top chart for a city. Therefore, the most important songs have the lowest Importance Scores.

User Input Options: Through the Google Spreadsheet, users have 3 input options to customize the Number of Top Songs and Unranked Song Score (these parameters are important for calculating the song's Importance Score) and whether to receive daily emails:

* Number of Top Songs: The "n" top songs the user wants to capture for each city. The maximum is 50. The script will change any input greater than 50 to 50.

* Unranked Song Score: The user-inputted value that increases the Importance Score for songs that do not rank in the top chart for a city. The minimum value for this input is 1 because the unranked song cannot be ranked equal or higher than the lowest ranked song in the city's top song chart. The script will change any input lower than 1 to 1.

* Pause Emails (Y/N): Type in Y to pause automated emails and N to send emails (case-sensitive).

Data Collection Method: Data/rankings are collected using Selenium/webscraping.

Front-End Interactives/Graphics: Dynamic tables and graphs are located in the auto-generated Google Sheet (if the charts display no data, it is due to a change in the most important songs for the day from the previous day. Use the table's drop-down menu to select a song from the updated list).

Automation: The script is automated using cron jobs.
