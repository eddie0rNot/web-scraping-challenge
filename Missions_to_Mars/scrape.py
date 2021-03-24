#!/usr/bin/env python
# coding: utf-8

# In[21]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from flask import Flask, render_template
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[3]:


# Define database and collection
db = client.nasa_db
collection = db.articles


# In[4]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news'

# Retrieve page with the requests module
response = requests.get(url)
# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())


# In[5]:


# Retrieve the parent divs for all articles
results = soup.find_all('div', class_='slide')

# loop over results to get article data
for result in results:
    # scrape the article header 
    news_title = result.find('div', class_='content_title').text
    
    # scrape the article subheader
    news_p = result.find('div', class_='rollover_description_inner').text
    
    # scrape the datetime
    #datetime = result.find('span', class_='article-item__date')['data-date'] 
    
    # get only the date from the datetime
    #date = datetime.split('T')[0]
    
    # print article data
    print('-----------------')
    print(news_title)
    print(news_p)

    # Dictionary to be inserted into MongoDB
    nasa_post = {
        'News Title': news_title,
        'Article Text': news_p
    }

    # Insert dictionary into MongoDB as a document
    collection.insert_one(nasa_post)


# In[6]:


# Display the MongoDB records created above
articles = db.articles.find()
for article in articles:
    print(article)


# In[9]:


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[10]:


url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[11]:


#Save URL for featured image
featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars3.jpg'


# In[13]:


# Save URL for Mars Facts table 
mars_facts_url = 'https://space-facts.com/mars/'


# In[14]:


# Read and create table
tables = pd.read_html(mars_facts_url)
tables


# In[15]:


# Check tables type
type(tables)


# In[16]:


# Convert to dataframe
mars_facts_df = tables[0]
mars_facts_df.head()


# In[17]:


# Convert dataframe to html string
mars_facts_html_table = mars_facts_df.to_html()
mars_facts_html_table


# In[18]:


# Clean up string
mars_facts_html_table.replace('\n', '')


# In[19]:


# Save to file
mars_facts_df.to_html('mars_facts_table.html')


# In[20]:


# Hemisphere image urls dict
hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif"},
]


# In[ ]:




