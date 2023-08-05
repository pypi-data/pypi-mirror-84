#!/usr/bin/env python
# coding: utf-8

# In[1]:


def connect_twitter(connection_pw):    
    
    '''
    Function connects to Twitter using AccessTokens, Access Secret, Consumerkey and consumerecret
    information. 
    Returns a variable that authorizes twitter connection.
    
    '''      
    import tweepy
    import warnings
    warnings.filterwarnings('ignore')
    from datetime import date
    
    ACCESSTOKEN = '1014097837381111808-1ZmyTn9NwXhnlnH3rLJdjLg7WmwFTG'
    ACCESS_SECRET = 'siiC7b529NpcGT8uwopjOaauSRZoUQdlN38mLL0gX2TLK'
    CONSUMERKEY = 'ZSTjRgpSwrcpgLDqTug1tnHVS'
    CONSUMERSECRET = '2mfFBHGIV0OT7b5LbgWrAbBhoyr3tB7GiGTtCGiz0pN8S9EFKv'
    
    if connection_pw == 'rapt0r':
        auth = tweepy.OAuthHandler(CONSUMERKEY, CONSUMERSECRET)
        auth.set_access_token(ACCESSTOKEN, ACCESS_SECRET)
        api = tweepy.API(auth)
    
    return api


# In[2]:


def get_hashtag_tweets(hashtag):
    
    '''
    Input: get_hashtag_tweets('#WhatsNewToday')
    Returns: 100 tweets in #WhatsNewToday hashtag.
    
    '''
    import tweepy
    import warnings
    from datetime import date
    warnings.filterwarnings('ignore')
    
    CONSUMERKEY = 'ZSTjRgpSwrcpgLDqTug1tnHVS'
    CONSUMERSECRET = '2mfFBHGIV0OT7b5LbgWrAbBhoyr3tB7GiGTtCGiz0pN8S9EFKv'
    
    auth = tweepy.OAuthHandler(CONSUMERKEY, CONSUMERSECRET)

    original = []
    api = tweepy.API(auth, wait_on_rate_limit=True)

    today = date.today()
    q = hashtag; count = 150
    title = 'Sentiments on Twitter about '+ q + ' on ' + str(today)
    arutweets = api.search(q=q, count=count)
    for tweet in arutweets:
        original.append(tweet.text)
        print(tweet.text)


# In[3]:


def get_user_tweets(api, user):
    
    '''
    Input: 
    api: variable of output of the connect_twitter function
    get_user_tweets('@JohnDoe')
    Returns: 100 tweets by @JohnDoe
    
    '''
    import tweepy
    import warnings
    warnings.filterwarnings('ignore')
    from datetime import date
    
    CONSUMERKEY = 'ZSTjRgpSwrcpgLDqTug1tnHVS'
    CONSUMERSECRET = '2mfFBHGIV0OT7b5LbgWrAbBhoyr3tB7GiGTtCGiz0pN8S9EFKv'
    
    arutweets = api.user_timeline(user)
    original = []
    for tweet in arutweets:
        original.append(tweet.text)
        print(tweet.text)
    
    return arutweets


# In[9]:


def tweet_to_dataframe(tweet_object):
    
    '''
    Display extracted tweets to a pandas dataframe.
    Inputs:
    tweet_objects: variable assigned to output of get_user_tweets or get_hastag_tweets functions.
    text = name assigned to the column of extracted tweets
    
    Returns: Dataframe
    '''
    
    import pandas as pd
    
    tweets = []    
    for tweet in tweet_object:

        text = tweet.text        
        tweets.append({'text':text})
    
    
    df = pd.DataFrame(tweets, columns=['text'])
    
    return df


# In[19]:


def text_preprocessing(dtf, punc=True, handle=True, https=True, 
                      hashtag=True, lower=True, strip=True, shortw=False, rt=True,
                     ): 
    
    '''
    This function cleans the raw text data by preprocessing.
    punc - will remove all punctuations from text
    handle - will remove all twitter handles or @ before twitter user names
    https - will remove all URLs
    hashtag - will remove all # signs
    lower - will convert text to lower
    strip - will remove end whitespaces
    rt - will remove RT from tweets or text
    shortw - will remove short words with letters less than 4 per word
    
    '''
    
    import string
    import re
    
    # Removal of all punctuation            
    if punc: dtf['text'] = dtf['text'].map(lambda x: re.sub('[,\.!?/*~`;^]:', '', x)) 
    
    # Removal of @, Links/URLs, RT and conversion to lower case.
    for i in dtf.text:        
        if handle: dtf['text'] = dtf['text'].str.replace('(@[\w]+)', '', regex=True)  # Handles
        if punc: dtf['text'] = dtf['text'].str.replace('([\w]:)', '', regex=True)  # Colon
        if punc: dtf['text'] = dtf['text'].str.replace('([\w] :)', '', regex=True)  # Colon
        if hashtag: dtf['text'] = dtf['text'].str.replace('(#[\w]+)', '', regex=True)  # Hash-tags
        if hashtag: dtf['text'] = dtf['text'].str.replace('(# [\w]+)', '', regex=True)  # Hash-tags
        
        if https: dtf['text'] = dtf['text'].str.replace                        ('((www\.[\s]+)|(https?://[^\s]+))', '', regex=True) # https
        if https: dtf['text'] = dtf['text'].str.replace                        ('((www\.[\s]+)|(http?://[^\s]+))', '', regex=True) # http
        
        
        if rt: dtf['text'] = dtf['text'].str.replace('RT', '', regex=True)        
        if lower: dtf.text = dtf['text'].str.lower() 
        if strip: dtf.text = dtf['text'].str.rstrip() 
        
        if punc: dtf['text'] = dtf['text'].str.replace("[^a-zA-Z#]", " ")   # more punctuations
        if shortw: dtf['text'] = dtf['text'].apply(
            lambda x: ' '.join([w for w in x.split() if len(w)>3]))    # remove short words       
        
        
    return dtf

