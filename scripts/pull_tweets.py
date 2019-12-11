import os 
import tweepy as tw
import pandas as pd
import json
import datetime
import re
from textblob import TextBlob 
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

def remove_stopwords(tweet) :
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(tweet)
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
  
    filtered_sentence = [] 
  
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
  
    return filtered_sentence

def remove_punctuation(tweet) :
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punct = ""
    for char in my_str:
        if char not in punctuations:
            no_punct = no_punct + char
    # display the unpunctuated string
    return no_punct

def get_tweets(handle='JoeBiden') :
    """
    Use the Twitter API to get tweets for a given Twitter handle. The default is Joe Biden. 
    The output is a JSON file of the tweets and timestamp. 
    For the purposes of this project, we have hardcoded a date of 05/01/19.
    """
    consumer_key = <consumer_key>
    consumer_secret = <consumer_secret>
    access_token = <access_token>
    access_token_secret = <access_token_secret>

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

def import_from_json(filename) :
    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)
    return data

def json_extract_text(json_data) :
    all_text = []
    for key in json_data.keys() : 
        all_text.append(json_data[key]['text'])
    return all_text



def main():
    """
    We will be pulling tweets
    """
    candidate_handles = ['JoeBiden', 'SenWarren', 'BernieSanders', 'PeteButtigieg', 'KamalaHarris']
    # other handles candidate_handles = ['AndrewYang', 'amyklobuchar']
    # for h in candidate_handles:
    #     get_tweets(handle=h)
    data = import_from_json("../SenSanders.json")
    text = json_extract_text(data)

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(text)

    true_k = 20
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)

    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        print("Cluster %d:" % i),
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind]),
        print

    try_to_guess = text[:4]
    for i in try_to_guess :
        Y = vectorizer.transform([i])
        prediction = model.predict(Y)
        print(i)
        print(prediction)


if __name__ == '__main__':
    main()
