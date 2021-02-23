##Elle Loveseth
##Purpose: 
##  Scrape article content from articles identified as having covid disinformation.
##  Append to existing training set of real and fake news.
##Updated: 2/22/2021

#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as beautsoup
import requests as req
import sklearn as sk

#initial training set data source: https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset
#includes two general datasets containing "true" news articles and "fake" news articles
#we'll use this as a baseline + add additional true and fake news articles scraped from the web to expand the dataset

#import datasets and code with a binary indicator variable to identify fake articles
training = pd.read_csv ('C://.../True.csv') #update with path to your file
training['fake'] = 0

fake = pd.read_csv ('C://.../Fake.csv') #update with path to your file
fake['fake'] = 1

#append datasets and code with binary indicator to identify covid-related articles
#this dataset only contains pre-covid articles, so it is coded accordingly
training = training.append(fake)
training['covid'] = 0
print(training)

#we'll now scrape fake covid-19 articles using BeautifulSoup
#first, we'll upload a table of links to fake articles and their source
articles = pd.read_csv ('C://.../fake_covid.csv') #update with path to your file

#create lists of each column to use in the for loop
articles_list = list(articles['url'])
source_list = list(articles['source'])

#to scrape articles, we need to identify the appropriate class code within the website's html code
#we inspect the website code source and track the class code in a dictionary corresponding with the article source
class_dictionary = {'Great Game India' : 'td-post-content lazyload',
                    'Infowars' : 'text' ,
                    'Health Impact News' : 'post-content',
                    'Freedom Articles' : 'simple-text size-4 tt-content title-droid margin-big' }

#create loop to scrape and compile articles
title_list = []
text_list = []
time_list = []

for num in np.arange(0, len(articles_list)) :
    
    #identify the url by position
    url = articles_list[num]
    
    #scrape the title of the article and append to list of titles
    html = req.get(url).text
    soup = beautsoup(html, 'html.parser')
    title = soup.find('title').get_text()
    title_list.append(title)
        
    #to scrape the content, we'll identify the class code using our dictionary and the article source
    source = source_list[num]
    class_key = class_dictionary[source]

    #scrape all content paragraphs from the article
    article = req.get(url)
    content = article.content
    soup = beautsoup(content, 'html5lib')
    content = soup.find_all('div', class_= class_key)
    content = content[0].find_all('p')

    #join all paragraphs together into one string and append to list of article text
    paragraphs = []
    for p in np.arange(0, len(content)) :
        paragraph = x[p].get_text()
        paragraphs.append(paragraph)
        full_article = " ".join(paragraphs)
    text_list.append(full_article)

#join list of titles and list of text into one pandas dataframe, then code with binary indicators
scraped_articles = pd.DataFrame(list(zip(title_list, text_list)),
                               columns =['title', 'text'])
scraped_articles['fake'] = 1
scraped_articles['covid'] = 1

print(scraped_articles)

#in the next update, we'll scrape true covid articles and join our datasets into a complete training set for analysis.

