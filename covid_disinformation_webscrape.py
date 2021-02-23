#!/usr/bin/env python
# coding: utf-8

# In[123]:


#!pip install beautifulsoup4
#!pip install requests

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as beautsoup
import requests as req
import sklearn as sk


# In[2]:


#initial training set data source: https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset
#includes two general datasets containing "true" news articles and "fake" news articles
#we'll use this as a baseline + add additional true and fake news articles scraped from the web to expand the dataset

training = pd.read_csv ('C://users/elove/Dropbox/Projects/Covid Disinformation/True.csv')
training['fake'] = 0

fake = pd.read_csv ('C://users/elove/Dropbox/Projects/Covid Disinformation/Fake.csv')
fake['fake'] = 1

training = training.append(fake)
training['covid'] = 0
print(training)


# In[155]:


#scrape fake covid-19 articles using BeautifulSoup

articles = pd.read_csv ('C://users/elove/Dropbox/Projects/Covid Disinformation/fake_covid.csv')
#articles = articles[articles['source'].isin(['Great Game India', 'Infowars', 'Freedom Articles'])]
#articles = articles.reset_index(drop = True)
articles_list = list(articles['url'])
source_list = list(articles['source'])

#create a dictionary that contains the class code for each source
class_dictionary = {'Great Game India' : 'td-post-content lazyload',
                    'Infowars' : 'text' ,
                    'Health Impact News' : 'post-content',
                    'Freedom Articles' : 'simple-text size-4 tt-content title-droid margin-big' }

#create loop to scrape and compile articles
title_list = []
text_list = []
time_list = []

for num in np.arange(0, len(articles_list)) :
        
    url = articles_list[num]
    html = req.get(url).text
    soup = beautsoup(html, 'html.parser')
    title = soup.find('title').get_text()
    title_list.append(title)
        
    #time = soup.find('time').get_text()
    #time_list.append(time)
        
    source = source_list[num]
    class_key = class_dictionary[source]

    article = req.get(url)
    content = article.content
    soup = beautsoup(content, 'html5lib')
    body = soup.find_all('div', class_= class_key)
    x = body[0].find_all('p')

    paragraphs = []
    for p in np.arange(0, len(x)) :
        paragraph = x[p].get_text()
        paragraphs.append(paragraph)
        final_article = " ".join(paragraphs)
        
    text_list.append(final_article)

scraped_articles = pd.DataFrame(list(zip(title_list, text_list)),
                               columns =['title', 'text'])
scraped_articles['fake'] = 1
scraped_articles['covid'] = 1

print(scraped_articles)


# In[140]:


time = soup.find('time')
print(time)

