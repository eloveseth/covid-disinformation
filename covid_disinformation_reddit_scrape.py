#!/usr/bin/env python
# coding: utf-8

# In[3]:


pip install praw
#!conda install -c conda-forge praw #did not use this; didn't work


# In[71]:


import pandas as pd
import sys
import praw as pr
import datetime as dt


# In[72]:


# access Reddit API
reddit = pr.Reddit(client_id='P169P55de-2B9w',                      client_secret='UcDGr8q-w_Nwo3Emr8DaXSsCY8Zg8w',                      user_agent='covid_disinformation',                      username='lola-the-spider',                      password='Freebie01!')


# In[73]:


#scrape post information (use later to scrape comments)



#access subreddit of choice
subreddits = ['Coronavirus', 'Conspiracy','CoronavirusFOS']

for subreddit in subreddits:
    subreddit = reddit.subreddit(subreddit)
    
    posts_id = []

    for post in subreddit.controversial(limit=10):
        posts_info.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])

posts_info = pd.DataFrame(posts_info,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

print(posts_info)
print(posts_id)


# In[74]:


#scrape associated comments--include all nested using commentForest
posts_id = posts_info["id"]
print(posts_id)

comments = []

for id in posts_id:
    submission = reddit.submission(id = id)
    submission.comments.replace_more(limit = None)

    for comment in submission.comments.list():
        comments.append([comment.body, id])

comments = pd.DataFrame(comments,columns=['comment', 'id'])
print(comments)
    


# In[ ]:




