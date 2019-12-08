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


with open('models/cluster_labels.json', 'r') as json_file:
    cluster_labels = json.load(json_file)
labels_dict = cluster_labels['cluster_titles']

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
    final_predictions = {}
    final_list = []
    for t in tweets_text:
        tweet = vectorizer.transform([t])
        pred_cluster = int(model.predict(tweet)[0])
        predictions_list.append(pred_cluster)
        print("Predicted_Cluster: {}".format(pred_cluster))

    for i in range(0, len(predictions_list)) :
        curr_predict = {}
        curr_predict['text'] = tweets_text[i]
        curr_predict['cluster'] = labels_dict.get("Cluster {}".format(predictions_list[i]))
        final_list.append(curr_predict)
    
    final_predictions['predictions'] = final_list
    return (final_predictions) 

def return_features(model=loaded_model, k=8):
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()

    features = {}
    for i in range(k):
        print("Cluster %d:" % i),
        term_list = []
        for ind in order_centroids[i, :10]:
            term_list.append(terms[ind])
        features["Cluster %d:" % i] = term_list
    return features