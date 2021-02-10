#!/usr/bin/env python
# coding: utf-8

#install praw using pip or conda
#pip install praw
#!conda install -c conda-forge praw

#import packages
import pandas as pd
import sys
import praw as pr
import datetime as dt

# access Reddit API
reddit = pr.Reddit(client_id='P169P55de-2B9w', #enter client id from Reddit API
                   client_secret='UcDGr8q-w_Nwo3Emr8DaXSsCY8Zg8w', #enter client secret from Reddit API
                   user_agent='covid_disinformation', #enter named user agent
                   username='USERNAME', #enter account username
                   password='PASSWORD!') #enter account password


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

#scrape associated comments and preserve submission id to link back to subreddit
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




