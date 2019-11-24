import os 
import tweepy as tw
import pandas as pd
import json
import datetime
import re
from textblob import TextBlob 

def get_tweets(handle='JoeBiden') :
    """
    Use the Twitter API to get tweets for a given Twitter handle. The default is Joe Biden. 
    The output is a JSON file of the tweets and timestamp. 
    For the purposes of this project, we have hardcoded a date of 05/01/19.
    """
    consumer_key = '7KEQmTV6fhm0mnmsyO9XNKPpx'
    consumer_secret = 'bevlcE2PiQAu0bMgSsBj1QrpOVdC3KGVyNvwu8A1rnlozLIUlq'
    access_token = '139221007-Oxzs1aPNr0pQefpVd5jeDfogKC9CktkiGityJGSJ'
    access_token_secret = '6EN5WAOCWH7E6avW9uomIvRYwQZfFxnBJS1yKCj3qJYRx'

    counter = 0
    final_dict = {}
    
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    for status in tw.Cursor(api.user_timeline, screen_name='@' + handle, tweet_mode="extended").items():
        print(status.created_at)
        curr_dict = {}
        curr_dict['text'] = status.full_text
        curr_dict['date'] = str(status.created_at)
        final_dict[counter] = curr_dict
        counter += 1
        end_date = datetime.datetime.strptime("05/01/19", "%m/%d/%y")
        if status.created_at < end_date :
            break

    path = 'data/' + handle + '.json'
    if not os.path.isfile(path):
        with open(path, 'w') as json_file:
            json.dump(final_dict, json_file)

def main():
    """
    We will be pulling tweets
    """
    candidate_handles = ['JoeBiden', 'SenWarren', 'BernieSanders', 'PeteButtigieg', 'KamalaHarris']
    # other handles candidate_handles = ['AndrewYang', 'amyklobuchar']
    for h in candidate_handles:
        get_tweets(handle=h)

if __name__ == '__main__':
    main()
