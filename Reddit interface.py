#! python3.
import urllib
import praw
import TwiterApi
from sys import path
from time import sleep
from random import shuffle

reddit = praw.Reddit(client_id='', \
                     client_secret='', \
                     user_agent='', \
                     username='', \
                     password='')

sleeptime = 6000
redditposts_cache = []
reddit_list = []
reddit_names = ['sub_a', 'sub_b']
for name in reddit_names:
    reddit_list.append(reddit.subreddit(name))
print(reddit_list)
keywords = ['discord', 'subreddit', '2018', '2019', '2020', 'month', 'discussion']

def textserch (text):
    text_2 = text.lower()
    for keyword in keywords:
        if keyword in text_2:
            return True
    return False

def testimage(imageurl):
    imagesplit = imageurl.split('.')
    if imagesplit[::-1][0] in ['jpg', 'png', 'tiff', 'bmp']:
        return True
    else:
        return False

def testitem(item):
    if item[1] == '' and testimage(item[2]):
        return True
    elif item[1] != '' and not testimage(item[2]):
        return True
    else:
        return False

def getsubbmision(submission):
    title = submission.title 
    body = submission.selftext 
    if textserch(title) or textserch(body) or not testitem([submission.title, submission.selftext, submission.url]):
        return 0
    title = title.replace('[Image] ', '')
    title = title.replace('[Video] ', '')
    title = title.replace('[Image]', '')
    title = title.replace('[Video]', '')
    submissionlist = [title, body, submission.url]
    return submissionlist

def getsubbmisions():
    redditposts_cache = []

    for reddit in reddit_list:
        print(reddit)
        reddithot = reddit.hot(limit=50)
        for submission in reddithot:
            sub = getsubbmision(submission)
            if sub != 0:
                redditposts_cache.append(sub)
    
    return redditposts_cache

def dl_img(url, filepath, filename):
    full_path = filepath + filename
    urllib.request.urlretrieve(url, full_path)

while True:
    allsubmisions = getsubbmisions()
    shuffle(allsubmisions)
    while len(allsubmisions) > 0:
        subbmision = allsubmisions.pop()
        print('-------------------------------------------')
        print(subbmision[0]+' '+subbmision[1])
        if testimage(subbmision[2]):
            url = subbmision[2]
            fileending = url.split('.')[::-1][0]
            try:
                dl_img(url, path[0], '\\temp.'+fileending)
            except:
                print('Dl Error')
                continue
            print(subbmision[0]+' '+subbmision[1])
            try:
                print(TwiterApi.sendtweetwithimage(subbmision[0]+' '+subbmision[1], path[0]+'\\temp.'+fileending))
            except:
                print('error image')
                continue
            sleep(sleeptime)
            #request image and tweet it
        else:
            try:
                print(TwiterApi.sendtweet(subbmision[0]+' '+subbmision[1]))
            except:
                print('error text')
                continue
                
            sleep(sleeptime)
            
