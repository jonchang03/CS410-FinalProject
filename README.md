# Tagging Categories of Democratic Candidate Tweets

## Use Case
The topic that we had originally proposed did not end up coming to fruition. As proposed, we grabbed 6 months of tweets of the top 5 democratic candidates in October (Buttigieg, Harris, Biden, Warren, Sanders). We then preprocessed the tweets, removing stopwords and punctuation, to get a narrower focus on what the content of the tweets. Sentiment analysis, using python's TextBlob library, was then performed. Our initial proposal was to compare the sentiment of the tweets with their polling numbers to determine if we could predict the future polling numbers of the candidate. Unfortunately, we were not able to find a strong enough correlation between polling numbers and tweet sentiment. 

We moved on to a stronger use case, involving democratic candidate tweets. One of Twitter's main objectives right now is preventing fake information, specifically about the candidates, from being posted on the platform. To go along with that trend, we thought it would be important for Twitter users to be able to figure out what political issue a candidate's tweet is relating to (i.e. climate change, student debt, etc...). Therefore, we decided to use clustering to determine the topics that were being talked about by the candidates in their tweets.

After analysis of the clusters, we were able to label them with broad categories every candidate has a stance on. These are:
    * Healthcare
    * Student Debt 
    * Trump
    * NEED TO FILL IN


One possible user of our tool could be Twitter itself, in order to learn as much information about political Tweets as possible.


## Software Discussion

### Methodology
The software is written primarily using two open-source libraries, Tweepy and sklearn. The tweepy libary is used to pull all metadata of tweets given a specifc user. We used it to collect all of our training data. 

The training data of all of the candidates is merged together. Each tweet is cleaned of any punctuation as to not be involved in any of the clustering. To prepare for training a model, we put the list of tweets through a tfidf vectorizer, ignoring the english stopwords. The vectorizer is then transformed. 

The model used is k-Means, with the number of clusters specified to 8, as we found the best results from this value. Once the clusters were created, we used manual intervention to give a topic label to each cluster. 

For testing purposes, the model that was generated using the collected twitter data is saved and ready for testing purposes. 

### Directory Layout
Below is an overview of our project files. The `data` directory contains the JSON files of the tweets that we pulled for the top 5 presidential candidates (at the time). We used these tweets to train our k-Means classifier and also pulled some samples for our example (below). The `docker` directory contains the `Dockerfile` and other necessary files to build a container running our app. Our `scripts` directory contains the python scripts necessary to run our Flask App and also contains *FinalProject.ipynb* where we did a lot of exploratory analysis (including our intial proposal of sentiment correlation). It also contains a `models` subdirectory which houses our serialized model and vectorizer which are used by our app. 
```
├── README.md
├── data
│   ├── BernieSanders.json
│   ├── JoeBiden.json
│   ├── KamalaHarris.json
│   ├── PeteButtigieg.json
│   └── SenWarren.json
├── docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── python_requirements.txt
├── scripts
│   ├── FinalProject.ipynb
│   ├── models
│   │   ├── final_prediction.pickle
│   │   └── final_vectorizer.pickle
│   ├── prediction.py
│   ├── pull_tweets.py
│   ├── server.py
│   └── start_flask.sh
└── to_predict_json.json
```

## How to Use
Note: For this tutorial, we assume that the user has Docker installed. For more information, please refer to the [Docker Docs](https://docs.docker.com/engine/reference/commandline/docker/).

Simply navigate to the docker folder:  
`cd docker`  
and run:  
`docker-compose up`  
Docker will use the included Dockerfile to build an image with the requirements specified in python_requirements.txt and serve the app on `localhost:5000`.

In a separate terminal, we can then send POST requests to our application. For the purposes of this demonstration, we decided to keep things simple and we only have 2 specific options.

##### GET /
**Description**: Will return `server is up` to indicate server is running
Usage: `curl -X GET  http://localhost:5000`

##### POST /predict_cluster 
**Description**: Will return a json object containing the sentences you that are being clustered and their predicted cluster.

We created a sample `to_predict_json.json` which gives us an idea of the expected format of the input JSON file. Users can easily modify this file and add as many tweets as they want for a batch prediction.

**Usage**: `curl -X POST -H "Content-Type: application/json" -d @to_predict_json.json http://localhost:5000/predict_cluster` (Note that this has to be run from the project directory which contains `to_predict_json.json`.)  
Expected Output: 

##### GET /get_cluster_titles

**Description**: Will return the titles of the cluster of preset model. For the project, the model is set to one that we generated and include in the `/models` folder. 

**Usage**: `curl -X GET  http://localhost:5000/get_cluster_titles`
**Expected Output For Project**: 
```
{
  "Cluster Titles": {
    "Cluster 0": "Cluster 0", 
    "Cluster 1": "Cluster 1", 
    "Cluster 2": "Cluster 2", 
    "Cluster 3": "Cluster 3", 
    "Cluster 4": "Cluster 4", 
    "Cluster 5": "Cluster 5", 
    "Cluster 6": "Cluster 6", 
    "Cluster 7": "Cluster 7"
  }
}
```

##### GET /get_cluster_features
**Description**: Will return a list of features for each cluster of preset model. For the project, the model is set to one that we generated and include in the `/models` folder. 

**Usage**: `curl -X GET  http://localhost:5000/get_cluster_features`
Expected Output
```
__NEED TO FILL OUT__
```
##### POST /label_clusters
**Description**: Use this endpoint to set titles for each of the clusters that are used. 

**Usage**:

```
curl -X POST -H "Content-Type: application/json" -d '{"Cluster 0": "Gun Control","Cluster 1": "Candidates","Cluster 2": "Human Rights","Cluster 3": "Health Care","Cluster 4": "Presidential Campaign","Cluster 5": "Trump","Cluster 6": "Wages","Cluster 7": "Climate Change"}' http://localhost:5000/label_clusters
```

The first HTTP request just checks that our server is up and running, and the second POST request allows us to actually send some JSON examples and receive predictions. 


## Contributions 

David Kiernicki - Scraped the twitter data and wrote the code to scrape, create docker image and base flask, wrote half of the clustering code. 

Jonathan Chang - Worked on correlation between sentiment and polling (no longer being used), wrote code for saving models and cluster names, and built out flask app.

## Acknowledgements
The following tutorials and resources were very helpful in our development process: 
* Pulling Twitter data: https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
* Twitter API and Developer Access: https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens
* k-Means API: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
* Flask App / Docker deployment: https://medium.com/dataswati-garage/deploy-your-machine-learning-model-as-api-in-5-minutes-with-docker-and-flask-8aa747b1263b
* Docker CLI commands: https://docs.docker.com/engine/reference/commandline/docker/