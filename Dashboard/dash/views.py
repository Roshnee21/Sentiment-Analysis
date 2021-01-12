from django.shortcuts import render

import matplotlib.pyplot as plt
import tweepy 
import numpy as np                                                                                                                                      
import pandas as pd
import seaborn as sns
import pandas.util.testing as tm
import math
import re
import xlsxwriter
import datetime
import time

# Create your views here.
def home(request):
        #all the libraries are imported 
    def livetweets():
        consumer_key = 'xxxxxxxxxxxxxxxxx' # enter your deatils for the developer account of Twitter
        consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

        # Creating the authentication object
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # Setting your access token and secret
        auth.set_access_token(access_token, access_token_secret)
        # Creating the API object while passing in auth information
        api = tweepy.API(auth)
        def datetime_from_utc_to_local(utc_datetime):
            now_timestamp = time.time()
            offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
            return utc_datetime + offset

        workbook = xlsxwriter.Workbook('C:/Users/Roshan Dadlani/Desktop/Projects/ibmdash/Dashboard/2020-04-16 Coronavirus Tweets.CSV')
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Source')
        worksheet.write('B1', 'Channel')
        worksheet.write('C1', 'Link')
        worksheet.write('D1', 'Title')
        worksheet.write('E1', 'Time of Post')
        format = workbook.add_format({'text_wrap': True})
        worksheet.set_column('C:D',30, format)
        worksheet.set_column('A:B',20, format)
        worksheet.set_column('E:E',30, format)

        row = 1
        col = 0




        for tweet in tweepy.Cursor(api.search,q=["#covid","#covid19","#coronavirus","#lockdown","#Wuhan","#pandemic","#quarantine","#outbreak","#vaccine","#corona","#stayhomestaysafe","#stayhome","#positive","#stay","#indiafightscorona","#fights","#deaths","#home"],
                                lang="en",
                                since="2020-06-21",exclude_retweets=True,
                                exclude_replies=True,
                                contributor_details=False,
                                include_entities=False).items(200):
            created_date_local = datetime_from_utc_to_local(tweet.created_at)
            print(f"{tweet.user.name} said: {tweet.text} at time:{created_date_local}")
            tweettext=tweet.text
            url=[]
            url=re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweettext)

            tweetuser=tweet.user.name
            tweettime=str(created_date_local)
            print(url)
            channel="twitter"
            data = ( [tweet.user.name, channel, url, tweettext, created_date_local],)
            for tweetuser, channel,url,tweet, tweettime in (data): 
                i=0
                worksheet.write(row, col, tweetuser) 
                worksheet.write(row,col + 1, channel)
                if url:
                    worksheet.write(row,col + 2, url[i])
                worksheet.write(row,col + 3, tweettext)
                worksheet.write(row,col + 4, tweettime)
                i+=1
                row += 1
        workbook.close()

        worksheet = pd.read_excel("C:/Users/Roshan Dadlani/Desktop/Projects/ibmdash/Dashboard/2020-04-16 Coronavirus Tweets.CSV")

    

    from textblob import TextBlob

    import re
    #to mount google drive inorder to load data
    

    from collections import Counter

    import warnings
    warnings.filterwarnings("ignore")

    import os
    for dirname, _, filenames in os.walk('/kaggle/input'):
        for filename in filenames:
            print(os.path.join(dirname, filename))

    # Reading data
    df=pd.read_csv('C:/Users/Roshan Dadlani/Desktop/Projects/ibmdash/Dashboard/2020-04-16 Coronavirus Tweets.CSV')
    # df.head()

    # display columns
    #df.columns

    # dropping columns
    tweet = df.copy()
    tweet.drop(['status_id','user_id','screen_name','source','reply_to_status_id','reply_to_user_id','is_retweet','place_full_name','place_type','reply_to_screen_name','is_quote','followers_count','friends_count','account_lang','account_created_at','verified'],axis=1, inplace = True)
    #tweet.head()

    # filtering data with 'country_code = IN' and 'language = en'
    tweet =tweet[(tweet.country_code == "IN") & (tweet.lang == "en")].reset_index(drop = True)
    tweet.drop(['country_code','lang'],axis=1,inplace=True)
    #tweet.head()

    # created_at column
    tweet["created_at"] = tweet["created_at"].apply(lambda i:(int(i.split("T")[1].split(":")[0])+int(i.split("T")[1].split(":")[1])/60))

    # shape
    tweet.shape

    # check missing values
    tweet.isna().sum()

    # data preprocessing
    for i in range(tweet.shape[0]) :
        tweet['text'][i] = ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(#[A-Za-z0-9]+)", " ", tweet['text'][i]).split()).lower()
    #tweet['text'].head()

    """**TOP 5 MOST FAVT TWEETS**"""

    # fav = tweet[['favourites_count','text']].sort_values('favourites_count',ascending = False)[:5].reset_index()
    # for i in range(5):
    #     print(i,']', fav['text'][i],'\n')

    """**TOP 5 MOST RETWEETED TWEETS**"""

    # retweet = tweet[['retweet_count','text']].sort_values('retweet_count',ascending = False)[:5].reset_index()
    # for i in range(5):
    #     print(i,']', retweet['text'][i],'\n')

    """**NUMBER OF TWEETS/HOUR**"""

    plt.figure(1, figsize=(10,6))
    plt.hist(tweet["created_at"],bins = 24)
    plt.xlabel('Hours',size = 15)
    plt.ylabel('No. of Tweets',size = 15)
    plt.title('No. of Tweets per Hour',size = 15)
    tweetperhr = list(tweet["created_at"])
    tweetperhrupdated = []
    tweetperhrcount = []
    count=0

    for i in range(len(tweetperhr)):
        if math.floor(tweetperhr[i]) not in tweetperhrupdated:
            tweetperhrupdated.append(math.floor(tweetperhr[i]))
 
    for i in range(24):
        count=0
        for j in range(len(tweetperhr)):
            if i == math.floor(tweetperhr[j]):
                count = count+1
        tweetperhrcount.append(count)
       
    
    tweetperhrupdated.insert(0,1)
    

    tweetperhrcount.insert(0,1)
    

    




    """**WORDCLOUD**"""
    tweettext = list(tweet['text'])

    

    """**REMOVING STOPWORDS**"""
    stopwords = {'a',  'about',  'above',  'after',  'again',  'against',  'all',  'also',  'am',  'an',  'and',  'any',  'are',  "aren't",  'as',  'at',  'be',  'because',  'been',  'before',  'being',  'below',  'between',  'both',  'but',  'by',  'can',  "can't",  'cannot',  'com',  'could',  "couldn't",  'did',  "didn't",  'do',  'does',  "doesn't",  'doing',  "don't",  'down',  'during',  'each',  'else',  'ever',  'few',  'for',  'from',  'further',  'get',  'had',  "hadn't",  'has',  "hasn't",  'have',  "haven't",  'having',  'he',  "he'd",  "he'll",  "he's",  'her',  'here',  "here's",  'hers',  'herself',  'him',  'himself',  'his',  'how',  "how's",  'however',  'http',  'i',  "i'd",  "i'll",  "i'm",  "i've",  'if',  'in',  'into',  'is',  "isn't",  'it',  "it's",  'its',  'itself',  'just',  'k',  "let's",  'like',  'me',  'more',  'most',  "mustn't",  'my',  'myself',  'no',  'nor',  'not',  'of',  'off',  'on',  'once',  'only',  'or',  'other',  'otherwise',  'ought',  'our',  'ours',  'ourselves',  'out',  'over',  'own',  'r',  'same',  'shall',  "shan't",  'she',  "she'd",  "she'll",  "she's",  'should',  "shouldn't",  'since',  'so',  'some',  'such',  'than',  'that',  "that's",  'the',  'their',  'theirs',  'them',  'themselves',  'then',  'there',  "there's",  'these',  'they',  "they'd",  "they'll",  "they're",  "they've",  'this',  'those',  'through',  'to',  'too',  'under',  'until',  'up',  'very',  'was',  "wasn't",  'we',  "we'd",  "we'll",  "we're",  "we've",  'were',  "weren't",  'what',  "what's",  'when',  "when's",  'where',  "where's",  'which',  'while',  'who',  "who's",  'whom',  'why',  "why's",  'with',  "won't",  'would',  "wouldn't",  'www',  'you',  "you'd",  "you'll",  "you're",  "you've",  'your',  'yours',  'yourself',  'yourselves',  's',  't',  'a',  'b',  'c',  'd',  'e',  'f',  'g',  'h',  'i',  'j','k','l','m','n','o','p','q','r','u','v','w','x','y','z'}

    tweet['text'] = tweet['text'].apply(lambda tweets: ' '.join([word for word in tweets.split() if word not in stopwords]))


    

    

    """**ANALYZING TEXT FOR SENTIMENT**"""

    tweet['sentiment'] = ' '
    tweet['polarity'] = None
    tweetpositive=0
    tweetnegative=0
    tweetneutral=0
    
    for i,tweets in enumerate(tweet.text) :
        blob = TextBlob(tweets)
        tweet['polarity'][i] = blob.sentiment.polarity
        if blob.sentiment.polarity > 0 :
            tweet['sentiment'][i] = 'positive'
            
            tweetpositive=tweetpositive+1
        elif blob.sentiment.polarity < 0 :
            tweet['sentiment'][i] = 'negative'
            tweetnegative=tweetnegative+1
        else :
            tweet['sentiment'][i] = 'neutral'
            tweetneutral=tweetneutral+1
    polarity = []
    for i,tweets in enumerate(tweet.text) :
        blob = TextBlob(tweets)
        polarity.append(blob.sentiment.polarity)
    
    tweettext1 = tweettext
    tweettext2 = tweettext
    polarity1 = polarity
    polarity2 = polarity
    polaritypositive = [] 
    polaritynegative = []
    positivetweets= []
    negativetweets = []
    for i in range(0, 5):  
        max1 = 0
        tweetpositivity = 0 
        for j in range(len(polarity1)):      
            if polarity1[j] > max1: 
                max1 = polarity1[j] 
                tweetpositivity = tweettext1[j] 
        tweettext1.remove(tweetpositivity)
        positivetweets.append(tweetpositivity)
        polarity1.remove(max1) 
        polaritypositive.append(max1) 

   

    for i in range(0, 5):  
        min1 = 0
        tweetnegativity = 0 
        for j in range(len(polarity2)):      
            if polarity2[j] < min1: 
                min1 = polarity2[j] 
                tweetnegativity = tweettext2[j] 
        tweettext2.remove(tweetnegativity)
        negativetweets.append(tweetnegativity)
        polarity2.remove(min1) 
        polaritynegative.append(min1)

    


    """**SENTIMENT DISTRIBUTION**"""

    plt.figure(figsize=(10,6))
    sns.distplot(tweet['polarity'], bins=30)
    plt.title('Sentiment Distribution',size = 15)
    plt.xlabel('Polarity',size = 15)
    plt.ylabel('Frequency',size = 15)

    """**Using Word Clouds to see the higher fequency words from each sentiment**"""

    
    

    count = pd.DataFrame(tweet.groupby('sentiment')['favourites_count'].sum())
    count.head()

    """**Most frequently appearing words**"""

    words = []
    words = [word for i in tweet.text for word in i.split()]

    freq = Counter(words).most_common(30)
    freq = pd.DataFrame(freq)
    freq.columns = ['word', 'frequency']
    
    word1=[]
    freq1=[]
    freq1=list(freq['frequency'])
    freq1.insert(0,1)
    freq1.insert(-1,1)
    word1=list(freq['word'])
    word1.insert(0,1)
    word1.insert(-1,1)
    
    plt.figure(figsize = (10, 10))
    

      
    return render(request, 'charts.html',{"positivetweets":positivetweets,"negativetweets":negativetweets,"tweetperhrcount":tweetperhrcount,"tweetperhr":tweetperhrupdated,"commonword":word1,"commonfreq":freq1,"tweetpositive":tweetpositive,"tweetnegative":tweetnegative,"tweetneutral":tweetneutral})














