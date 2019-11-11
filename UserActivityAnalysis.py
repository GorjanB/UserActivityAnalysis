#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np
import pandas as pd
import matplotlib as plot
import matplotlib.pyplot as plt

data = pd.read_csv('UserEventData.csv', delimiter = ',')


# In[196]:


data


# In[207]:


#1. How many unique users played the app
unique_users_count = len(data['AppsFlyer ID'].unique())
print(unique_users_count)


# In[208]:


#2. On which date was the highest activity (unique users played)
event_time = data['Event Time']
d = {}
for time in event_time:
    date = time.split()[0]
    d[date] = 0
    
date_users = data[['Event Time', 'AppsFlyer ID']]

def get_date(datetime):
    date = datetime.split()[0]
    return date

pd.options.mode.chained_assignment = None
date_users['Event Time'] = date_users['Event Time'].apply(get_date)

for date in d.keys():
    d[date] = len(date_users[date_users['Event Time'] == date]['AppsFlyer ID'].unique())
    
import operator
print(max(d.items(), key=operator.itemgetter(1))[0])


# In[209]:


# 3. How many users upgraded the app from version 1.8.3 to 1.9
data_latest_versions = data[(data['App Version'] == '1.8.3') | (data['App Version'] == '1.9')]

d_users = {}
for appid in data_latest_versions['AppsFlyer ID']:
    d_users[appid] = 0
    
for user in d_users.keys():
    d_users[user] = len(data_latest_versions[data_latest_versions['AppsFlyer ID'] == user]['App Version'].unique())
    
print(list(d_users.values()).count(2))


# In[210]:


# 4. Provide BAr chart of # of users across country
d_countries = {}
countries = data['Country Code']

for country in countries:
    d_countries[country] = 0
    
for country in list(d_countries.keys()):
    d_countries[country] = len(data[data['Country Code'] == country]['AppsFlyer ID'].unique())

N = len(list(d_countries.keys()))
users = list(d_countries.values())

#Variables
ind = np.arange(N)
width = 0.5

fig = plt.figure(figsize = (25,15))
ax = fig.add_subplot(111)

## the bars
rects1 = ax.bar(ind, users, width,
                color='black',
                error_kw=dict(elinewidth=2,ecolor='red'))

# axes and labels
ax.set_xlim(-width,len(ind)+width)
ax.set_ylim(0, max(list(d_countries.values())))
ax.set_ylabel('Number of users')
ax.set_title('Unique users by country')
#xTickMarks = ['Group'+str(i) for i in range(1,6)]
countries = list(d_countries.keys())
xTickMarks = countries

ax.set_xticks(ind+width)
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)

## add a legend
#ax.legend( rects1[0], 'Countries')

plt.show()


# In[2]:


# 5. Provide a graph of dist of unique users vs #unique DMA
d_DMA = {}
DMA = data[data['DMA'] != 'None']['DMA']

for dma in DMA:
    d_DMA[dma] = 0
    
for dma in list(d_DMA.keys()):
    d_DMA[dma] = len(data[data['DMA'] == dma]['AppsFlyer ID'].unique())

#print(d_DMA)

data = {'DMA': list(d_DMA.keys()), 'Users': list(d_DMA.values())}
pd.DataFrame.from_dict(data, orient='index')


# In[212]:


# 6. How many distinct players use iphone vs how many players play ipad
d_players = {}
players = list(data['AppsFlyer ID'].unique())
iphone = 0
ipad = 0

for player in players:
    device = data[data['AppsFlyer ID'] == player]['Device Type'].unique()
    device = device[0].split()[0]
    if device == 'iPhone':
        iphone += 1
    else :
        if device == 'iPad':
            ipad += 1
        
print (ipad,"ipad",iphone,"iphone")


# In[213]:


# 7. Which user/users  is most active in terms of playing days
date_users = data[['Event Time', 'AppsFlyer ID']]

def get_date(datetime):
    date = datetime.split()[0]
    return date

date_users['Event Time'] = date_users['Event Time'].apply(get_date)

d_users = {}
for user in date_users['AppsFlyer ID']:
    d_users[user] = 0
    
for user in date_users['AppsFlyer ID']:
    d_users[user] = len(date_users[date_users['AppsFlyer ID'] == user]['Event Time'].unique())
  
import operator
max_result = max(d_users.items(), key=operator.itemgetter(1))
print("user",max_result[0],"played",max_result[1],"days")


# In[7]:


#Retention prediction
#Please try to estimate the likelihood of a user to come back and play the game more than one day
#Based on his first day activity (# events on day of install)

def get_date(datetime):
    date = datetime.split()[0]
    return date

data['Install Time'] = data['Install Time'].apply(get_date)
data['Event Time'] = data['Event Time'].apply(get_date)


# In[8]:


users_startdate = {}
for user in data['AppsFlyer ID']:
    #users_startdate[user] = data[data['AppsFlyer ID'] == user]['Install Time'].unique()[0]
    users_startdate[user] = data[data['AppsFlyer ID'] == user]['Install Time'].iloc[0]
    
users_startdate


# In[9]:


users_eventsOnstartdate = {}
for user in list(users_startdate.keys()):
    users_eventsOnstartdate[user] = len(data[(data['AppsFlyer ID'] == user) & (users_startdate[user] == data['Event Time'])]['Event Time'])


# In[10]:


users_eventsOnstartdate


# In[13]:


count = 0
print("Insert number of events on day of install:")
X = int(input())
print("Insert value for neighbor span")
k = int(input())
a = X - k
b = X + k
total = 0

for user in list(users_startdate.keys()):
    events = users_eventsOnstartdate[user]
    
    if (events >= a) & (events <= b):
        total+=1
        for date in list(data[data['AppsFlyer ID'] == user]['Event Time']):
            if date != users_startdate[user]:
                count+=1
                break

print("The probability that a user with ",X,"events on day of install with a span of",k,"is:",count/total)


# In[ ]:




