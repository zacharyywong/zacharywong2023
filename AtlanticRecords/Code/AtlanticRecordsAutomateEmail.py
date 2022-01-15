#!/usr/bin/env python
# coding: utf-8

# In[1]:


import email, ssl, smtplib

#from email import encoders

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase

from datetime import date


# In[2]:


subject = 'Top 5 Most Important Songs of the Day'
text = 'Hi Jake and the team, here is a CSV attachment with the 5 most important songs of the day you should look out for.'
sender_email = "zacharywongdatascience"
receiver_email = 'zachary.j.wong.23@dartmouth.edu'
password = 'ekxftlkowfajcuhn'
filename = 'Top5ImportantSongs-' + str(date.today()) +'.csv'


# In[3]:


msg = MIMEMultipart()
msg ["From"] = sender_email
msg ["To"] = receiver_email
msg ["Subject"] = subject

msg.attach(MIMEText(text, "plain"))

filepath = '/Users/zacharywong/github/zacharywong2023/AtlanticRecords/Deliverable-Top5ImportantSongs.csv'

with open (filepath, 'rb') as file:
    msg.attach(MIMEApplication(file.read(), Name=filename))

    #part = MIMEBase("application", "octet-stream")
    #part.set_payload(file.read())

#encoders.encode_base64(part)
msg['Content Disposition'] = "attachment; filename=Top5ImportantSongs"
#msg.attach(part)
content = msg.as_string()

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, content)






# In[ ]:





# In[ ]:




