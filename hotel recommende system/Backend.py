#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from matplotlib import pyplot
import seaborn as sns
# get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


# In[3]:


hotel_detail = pd.read_csv('Hotel_details.csv', delimiter=',')
hotel_rooms = pd.read_csv('Hotel_Room_attributes.csv', delimiter=',')

hotel_detail.head()

hotel_rooms.head()

hotel_detail.columns

hotel_rooms.columns


# In[4]:


hotel_rooms.info()

hotel_detail.info()

hotel_detail.describe()

hotel_rooms.describe()


# In[5]:


del hotel_detail['id']
del hotel_rooms['id']
del hotel_detail['zipcode']
del hotel_detail['latitude']
del hotel_detail['longitude']


# In[6]:


hotel_detail = hotel_detail.dropna()
hotel_rooms = hotel_rooms.dropna()

hotel_detail.drop_duplicates(subset='hotelid', keep=False, inplace=True)


# In[7]:


hotel = pd.merge(hotel_rooms, hotel_detail, left_on='hotelcode', right_on='hotelid', how='inner')

hotel.columns


# In[8]:


hotel['description'] = hotel['roomamenities'] + hotel['ratedescription']

del hotel['ratedescription']
del hotel['roomamenities']


# In[9]:


hotel.columns

hotel.describe(include='all')

sum(hotel.duplicated())

hotel_after_removing_duplicates = hotel.drop_duplicates()

sum(hotel_after_removing_duplicates.duplicated())

# check for missing value

hotel = hotel_after_removing_duplicates.dropna()

hotel.describe()


# In[10]:


numeric_columns = hotel.select_dtypes(include=[np.number]).columns
corr_df = hotel[numeric_columns].corr(method="pearson")

pyplot.figure(figsize=(9, 6))
heatmap = sns.heatmap(corr_df, annot=True, fmt=".1g", vmin=-1, vmax=1, center=0, cmap="rocket", linewidths=1, linecolor="black")
heatmap.set_title("Correlations HeatMap between variables")
heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=90)


# In[11]:


pyplot.figure(figsize = (15, 7))
sns.regplot(data = hotel, y = "price", x = "starrating", color = "r").set(title = "Price'vs Rating correlation")


# In[12]:


plot = hotel[["hotelname", "starrating"]].drop_duplicates()
sns.set(font_scale = 2.5)
a4_dims = (15, 7)
fig, ax = pyplot.subplots(figsize = a4_dims)
sns.countplot(ax = ax, x = "starrating", data = plot);


# In[13]:


hotel_counts = hotel["hotelname"].value_counts()
hotel_counts[:10].plot(kind = 'barh', figsize = (20, 8));


# **graph showing count of hotels**

# In[14]:


plot = hotel[["city", "country"]].drop_duplicates()
plot.groupby('country').count()
sns.set(font_scale = 1.8)
a4_dims = (15, 7)
fig, ax = pyplot.subplots(figsize = a4_dims)
pyplot.xticks(rotation = 90)
sns.countplot(ax = ax, x = "country", data = plot).set(title = "Number of hotels in each country");


# # Recommender system based only on city and ratings about the hotel

# In[15]:


def citybased(city):
    hotel['city'] = hotel['city'].str.lower()
    citybase = hotel[hotel['city'] == city.lower()]
    citybase = citybase.sort_values(by = 'starrating', ascending = False)
    citybase.drop_duplicates(subset = 'hotelcode', keep = 'first', inplace = True)
    if(citybase.empty == 0):
        hname = citybase[['hotelname', 'price', 'starrating', 'address', 'description','url']]
        return hname.head(10)
    else:
        print('No Hotels Available')


# In[16]:


citybased('london')


# # Requirment and special needs based recommender

# In[17]:


def pop_citybased(city, number):
    hotel['city'] = hotel['city'].str.lower()
    popbased = hotel[hotel['city'] == city.lower()] 
    popbased = popbased[popbased['guests_no'] == number].sort_values(by='starrating', ascending=False)
    popbased.drop_duplicates(subset='hotelcode', keep='first', inplace=True)
    if popbased.empty:
        print('Sorry No Hotels Available\n tune your constraints')
    else:
        return popbased[['hotelname', 'price', 'roomtype', 'guests_no', 'starrating', 'address', 'description', 'url']].head(10)

        


# In[18]:


pop_citybased('paris', 2)


# In[19]:


hotel.head()


# In[20]:


hotel['description'] = hotel['description'].str.replace(': ;',',')


# In[21]:


hotel['description']


# In[22]:


def requirementbased(city, number, features):
    hotel['city'] = hotel['city'].str.lower()
    hotel['description'] = hotel['description'].str.lower()
    features = features.lower()
    features_tokens = word_tokenize(features)
    sw = stopwords.words('english')
    lemm = WordNetLemmatizer()
    f1_set = {w for w in features_tokens if not w in sw}
    f_set = set()
    for se in f1_set:
        f_set.add(lemm.lemmatize(se))
    reqbased = hotel[hotel['city'] == city.lower()]
    reqbased = reqbased[reqbased['guests_no'] == number].sort_values(by='starrating', ascending=False)
    cos = []

    for i in range(reqbased.shape[0]):
        temp_tokens = word_tokenize(reqbased['description'].iloc[i])
        temp1_set = {w for w in temp_tokens if not w in sw}
        temp_set = set()
        for se in temp1_set:
            temp_set.add(lemm.lemmatize(se))
        rvector = temp_set.intersection(f_set)
        cos.append(len(rvector))
        
    reqbased['similarity'] = cos
    reqbased = reqbased.sort_values(by='similarity', ascending=False)
    reqbased.drop_duplicates(subset='hotelcode', keep='first', inplace=True)
    return reqbased[['hotelname', 'roomtype', 'price', 'guests_no', 'starrating', 'address', 'description', 'similarity', 'url']].head(10)


# print(requirementbased('london', 4, 'I need a extra toilet and air condition'))

# # pricing

# In[23]:


def recommender(city, number, features, price):
    hotel['city'] = hotel['city'].str.lower()
    hotel['description'] = hotel['description'].str.lower()
    features = features.lower()
    features_tokens = word_tokenize(features)
    sw = stopwords.words('english')
    lemm = WordNetLemmatizer()
    f1_set = {w for w in features_tokens if not w in sw}
    f_set = set()
    for se in f1_set:
        reqbased = hotel[hotel['city'] == city.lower()]
    reqbased = reqbased[reqbased['guests_no'] == number]
    reqbased = reqbased[reqbased['price'] <= price].sort_values(by='starrating', ascending=False)
    reqbased = reqbased.set_index(np.arange(reqbased.shape[0]))
    
    cos = []  # Initialize the cosine similarity list here
    
    for i in range(reqbased.shape[0]):
        temp_tokens = word_tokenize(reqbased['description'].iloc[i])
        temp1_set = {w for w in temp_tokens if not w in sw}
        temp_set = set()
        for se in temp1_set:
            temp_set.add(lemm.lemmatize(se))
        rvector = temp_set.intersection(f_set)
        cos.append(len(rvector))

    # Check if the length of cos matches the number of rows in the DataFrame
    if len(cos) == reqbased.shape[0]:
        reqbased['similarity'] = cos
        reqbased = reqbased.sort_values(by='similarity', ascending=False)
        reqbased.drop_duplicates(subset='hotelcode', keep='first', inplace=True)
        return reqbased[['hotelname', 'roomtype', 'price', 'guests_no', 'starrating', 'address', 'description', 'similarity', 'url']].head(10)
    else:
        print("Error: Length of cosine similarity list does not match the number of rows in DataFrame.")


# In[24]:


recommender('london', 2, 'I need free wifi and breakfast', 1000)


# # Export dataframe

# In[25]:


hotel.to_csv('hotes-info.csv')


# In[ ]:




