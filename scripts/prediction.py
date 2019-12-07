import pandas as pd
import numpy as np
import pickle 
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import re   

# load the model from disk
model_path = 'models/final_prediction.pickle'
vectorizer_path = 'models/final_vectorizer.pickle'
loaded_model = pickle.load(open(model_path, 'rb'))
vectorizer = pickle.load(open(vectorizer_path, 'rb'))

def clean_tweet(tweet):
    '''
    Cleans tweet text by removing links,
    special characters - using regex statements.
    '''
    # In case you forget: you removed the (@[A-Za-z0-9]+)| reg ex.
    # useful site: http://regexr.com/
    return ' '.join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def make_prediction(input_json, model=loaded_model):
    json_data = json.loads(json.dumps(input_json))
    tweets_text = []
    for key in json_data.keys() : 
        clean_text = json_data[key]['text']
        print(key, clean_tweet(clean_text))
        tweets_text.append(clean_text)
        
    predictions_list = []
    for t in tweets_text:
        tweet = vectorizer.transform([t])
        pred_cluster = int(model.predict(tweet)[0])
        predictions_list.append(pred_cluster)
        print("Predicted_Cluster: {}".format(pred_cluster))
    return (predictions_list) # can maybe map to dictionary