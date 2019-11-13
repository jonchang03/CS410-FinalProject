import os 
import tweepy as tw
import pandas as pd
import json
import datetime
import re
from textblob import TextBlob 

consumer_key = '7KEQmTV6fhm0mnmsyO9XNKPpx'
consumer_secret = 'bevlcE2PiQAu0bMgSsBj1QrpOVdC3KGVyNvwu8A1rnlozLIUlq'
access_token = '139221007-Oxzs1aPNr0pQefpVd5jeDfogKC9CktkiGityJGSJ'
access_token_secret = '6EN5WAOCWH7E6avW9uomIvRYwQZfFxnBJS1yKCj3qJYRx'


counter = 0
final_dict = {}

def get_tweets() :
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    for status in tw.Cursor(api.user_timeline, screen_name='@JoeBiden', tweet_mode="extended").items():
        print(status.created_at)
        curr_dict = {}
        curr_dict['text'] = status.full_text
        curr_dict['date'] = str(status.created_at)
        final_dict[counter] = curr_dict
        counter += 1
        end_date = dt.strptime("05/01/19", "%m/%d/%y")
        if status.created_at < end_date :
            break

    with open('JoeBiden.json', 'w') as json_file:
        json.dump(final_dict, json_file)



def clean_tweet(tweet): 
    ''' 
    Utility function to clean tweet text by removing links, special characters 
    using simple regex statements. 
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 


def get_tweet_sentiment(tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(clean_tweet(tweet)) 
        # set sentiment 
        return analysis.sentiment.polarity
        # if analysis.sentiment.polarity > 0: 
        #     return 'positive'
        # elif analysis.sentiment.polarity == 0: 
        #     return 'neutral'
        # else: 
        #     return 'negative'

def sentiment_by_days(start_date, num_of_days, tweets) :
    tweet_count = 0 
    sentiment_sum = 0 
    start = start_date
    end = start_date  + datetime.timedelta(days=num_of_days)
    print(start)
    print(end)
    for key, value in tweets.items():
        curr_date = datetime.datetime.strptime(value['date'], "%Y-%m-%d %H:%M:%S")
        if curr_date >= start and curr_date < end : 
            tweet_count += 1 
            sentiment_sum += get_tweet_sentiment(value['text'])
    return sentiment_sum / tweet_count



with open('warren3.json') as json_file:
    data = json.load(json_file)


curr_date = datetime.datetime.strptime("05/01/19", "%m/%d/%y")
complete_date = datetime.datetime.strptime("11/01/19", "%m/%d/%y")
sent_dict = {}
while(curr_date < complete_date) :
    curr_sent = sentiment_by_days(curr_date, 7, data) 
    end_date = curr_date  + datetime.timedelta(days=7)
    sent_dict[str(end_date)]  = curr_sent
    curr_date += datetime.timedelta(days=7)
print(sent_dict)

with open('warrensent.json', 'w') as json_file:
        json.dump(sent_dict, json_file)