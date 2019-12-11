# Tagging Categories of Democratic Candidate Tweets

## Use Case
The topic that we had originally proposed did not end up coming to fruition. As proposed, we grabbed 6 months of tweets of the top 5 democratic candidates in October (Buttigieg, Harris, Biden, Warren, Sanders). We then preprocessed the tweets, removing stopwords and punctuation, to get a narrower focus on what the content of the tweets. Sentiment analysis, using python's TextBlob library, was then performed. Our initial proposal was to compare the sentiment of the tweets with their polling numbers to determine if we could predict the future polling numbers of the candidate. Unfortunately, we were not able to find a strong enough correlation between polling numbers and tweet sentiment. 

We moved on to a stronger use case, involving democratic candidate tweets. One of Twitter's main objectives right now is preventing fake information, specifically about the candidates, from being posted on the platform. To go along with that trend, we thought it would be important for Twitter users to be able to figure out what political issue a candidate's tweet is relating to (i.e. climate change, student debt, etc...). Therefore, we decided to use clustering to determine the topics that were being talked about by the candidates in their tweets.

After analysis of the clusters, we were able to label them with broad categories every candidate has a stance on (e.g. healthcare, student debt, climate change, etc..).

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
## Quickstart (see section below for detailed instructions)
**Note: For this tutorial, we assume that the user has Docker installed. For more information, please refer to the [Docker Docs](https://docs.docker.com/engine/reference/commandline/docker/).**

1. FIrst, let's get our Flask server up and running. Simply navigate to the docker folder:  
`cd docker`  
and run:  
`docker-compose up`  
Docker will use the included Dockerfile to build an image with the requirements specified in python_requirements.txt and serve the app on `localhost:5000`.

2. Now, we can run some HTTP requests. First, let's look at the current cluster titles. We use a config file called `cluster_labels.json` in our `models` directory to keep track of our labels. By default, they are empty, and we have included a way for the user to determine cluster titles!
```
$ curl -X GET  http://localhost:5000/get_cluster_titles
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
3. Let's look at the top terms in each cluster to help us determine appropriate titles for each cluster. Our model contains 8 clusters total, and we can see from the sample output that the first cluster seems to be about healthcare and the second one about gun control and the Trump Administration. 
```
$ curl -X GET  http://localhost:5000/get_cluster_features
{
  "Cluster Features": {
    "Cluster 0:": [
      "care",
      "health",
      "access",
      "affordable",
      "https",
      "right",
      "plan",
      "medicare",
      "medicareforall",
      "need"
    ],
    "Cluster 1:": [
      "trump",
      "president",
      "gun",
      "donald",
      "https",
      "violence",
      "administration",
      "congress",
      "end",
      "need"
    ],
    .
    .
    . 
``` 
4. So let's go ahead and label our clusters. Based on our observations of the top terms in each cluster, we come up with labels and pass a json file with cluster names as shown below. We also run our get_cluster_titles again and see that indeed, the cluster titles have changed!
```
$ curl -X POST -H "Content-Type: application/json" -d '{"Cluster 0": "Health Care", "Cluster 1": "Gun Control & Trump Administration", "Cluster 2": "Education & Student Debt", "Cluster 3": "Democratic Candidates", "Cluster 4": "Workers Rights & Equality", "Cluster 5": "Electoral Issues", "Cluster 6": "Climate Change", "Cluster 7": "Middle Class & Equal Pay "}' http://localhost:5000/label_clusters

$ curl -X GET  http://localhost:5000/get_cluster_titles
{ 
  "Cluster Titles": {
    "Cluster 0": "Health Care",
    "Cluster 1": "Gun Control & Trump Administration",
    "Cluster 2": "Education & Student Debt",
    "Cluster 3": "Democratic Candidates",
    "Cluster 4": "Workers Rights & Equality",
    "Cluster 5": "Electoral Issues",
    "Cluster 6": "Climate Change",
    "Cluster 7": "Middle Class & Equal Pay "
  }
}
```

5. Finally, let's make some predictions. We run our predict_cluster command with a JSON-formatted tweet, and see that our model predicts that it is about *Democratic Candidates*, which does indeed seem to be the case.
```
$ curl -X POST -H "Content-Type: application/json" -d '{"0": {"text": "RT @pujanpatel_: Bernie is one of the only presidential candidates that cares about my voice, and the collective voice of the working class"}}' http://localhost:5000/predict_cluster
{
  "Predicted Clusters": {
    "predictions": [
      {
        "cluster": "Democratic Candidates",
        "text": "RT @pujanpatel_: Bernie is one of the only presidential candidates that cares about my voice, and the collective voice of the working class"
      }
    ]
  }
}
```


## API Documentation

### Send HTTP Requests
Assuming our Flask server is running, in a separate terminal, we can then send GET and POST requests to our application. 

#### 1. GET /
**Description**: Will return `server is up` to indicate server is running
Usage: `curl -X GET  http://localhost:5000`

#### 2. GET /get_cluster_titles

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

#### 3. GET /get_cluster_features
**Description**: Will return a list of features for each cluster of preset model. For the project, the model is set to one that we generated and include in the `/models` folder. 

**Usage**: `curl -X GET  http://localhost:5000/get_cluster_features`  
**Output** (*truncated for documentation purposes*):
```
{
  "Cluster Features": {
    "Cluster 0:": [
      "care",
      "health",
      "access",
      "affordable",
      "https",
      "right",
      "plan",
      "medicare",
      "medicareforall",
      "need"
    ],
        .
        .
        .
    "Cluster 7:": [
      "women",
      "class",
      "middle",
      "pay",
      "https",
      "tax",
      "work",
      "time",
      "teachers",
      "equal"
    ]
  }
}
```
#### 4. POST /label_clusters
**Description**: Use this endpoint to set titles for each of the clusters that are used. 

**Usage**:

```
curl -X POST -H "Content-Type: application/json" -d '{"Cluster 0": "Health Care", "Cluster 1": "Gun Control & Trump Administration", "Cluster 2": "Education & Student Debt", "Cluster 3": "Democratic Candidates", "Cluster 4": "Workers Rights & Equality", "Cluster 5": "Electoral Issues", "Cluster 6": "Climate Change", "Cluster 7": "Middle Class & Equal Pay "}' http://localhost:5000/label_clusters
```

**Result**: `models/cluster_labels.json` will now look like:
```
{
    "model_name": "final_model",
    "cluster_titles": {
        "Cluster 3": "Democratic Candidates",
        "Cluster 0": "Health Care",
        "Cluster 6": "Climate Change",
        "Cluster 7": "Middle Class & Equal Pay ",
        "Cluster 1": "Gun Control & Trump Administration",
        "Cluster 2": "Education & Student Debt",
        "Cluster 5": "Electoral Issues",
        "Cluster 4": "Workers Rights & Equality"
    }
}
```

#### 5. POST /predict_cluster 
**Description**: Will return a json object containing the sentences you that are being clustered and their predicted cluster.

We created a sample `to_predict_json.json` which gives us an idea of the expected format of the input JSON file. Users can easily modify this file and add as many tweets as they want for a batch prediction.

**Usage**: `curl -X POST -H "Content-Type: application/json" -d @to_predict_json.json http://localhost:5000/predict_cluster` 

Note that this has to be run from the project directory which contains `to_predict_json.json`. This JSON file includes some sample tweets we pulled using our functions in our `pull_tweets.py` script.  

**Sample Output** (*truncated for documentation purposes*):
We see that we have the tweets and the predicted clusters they have been assigned to.
```
{
  "Predicted Clusters": {
    "predictions": [
      {
        "cluster": "Health Care",
        "text": "Many people are responding that they can't afford to get dental care. This is a major reason we need Medicare for All. Dental care is health care and Medicare for All covers it. https://t.co/OyfhL8mvek"
      },
      {
        "cluster": "Climate Change",
        "text": "Thousands of family farmers are forced off their land every year by big agribusinesses. It\u2019s time the government had the backs of family farmers instead of doing favors for corporate agriculture monopolies. https://t.co/ooyAU1ORva"
      }
      .
      .
      .
```

## Getting Twitter Credentials (not necessary for testing)
It isn't necessary get create twitter credentials to test our project. There are some sections in our jupyter notebook and python scripts that can assist with pulling data, if needed. Instructions for creating the credentials can be found [here](https://towardsdatascience.com/how-to-access-twitters-api-using-tweepy-5a13a206683b)

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
