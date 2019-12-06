## Tagging Categories of Democratic Candidate Tweets
### Use Case
The topic that we had originally proposed did not end up coming to fruition. As proposed, we grabbed 6 months of tweets of the top 5 democratic candidates in October (Buttigieg, Harris, Biden, Warren, Sanders). We then preprocessed the tweets, removing stopwords and punctuation, to get a narrower focus on what the content of the tweets. Sentiment analysis, using python's Textblob library, was then performed. Our proposal was to compare the sentiment of the tweets with their polling numbers to determine if we could predict the future polling numbers of the candidate. Unfortunately, we were not able to find a strong enough correlation between polling numbers and tweet sentiment. 

We moved on to a stronger use case, involving democratic candidate tweets. One of Twitter's main objectives right now is preventing fake information, specifically about the candidates, from being posted on the platform. To go along with that trend, we thought it would be important for Twitter users to be able to figure out what political issue a candidate's tweet is relating to (i.e. climate change, student debt, etc.). Therefore, we decided to use clustering to determine the topics that were being talked about by the candidates in their tweets.

After analysis of the clusters, we were able to label them with broad categories every candidate has a stance on. These are:
    1. Healthcare
    2. Student Debt 
    3. Trump
    4. NEED TO FILL IN


We see the user of tool being Twitter itself, to help give as much information about poltical Tweets as possible.


### Software

The software is written primarily using two open-source libraries, Tweepy and sklearn. The tweepy libary is used to pull all metadata of tweets given a specifc user. We used it to collect all of our training data. 

The training data of all of the candidates is merged together. Each tweet is cleaned of any punctuation as to not be involved in any of the clustering. To prepare for training a model, we put the list of tweets through a tfidf vectorizer, ignoring the english stopwords. The vecotrizer is then transformed. 

The model used is Kmeans, with the number of clusters specified to 8, as we found the best results from this value. Once the clusters were created, we used manual intervention to give a topic label to each cluster. 

For testing purposes, the model that was generated using the collected twitter data is saved and ready for testing purposes. 

### How to Use
_Documentation of the usage of the software including either documentation of usages of APIs or detailed instructions on how to install and run a software, whichever is applicable._

WORK IN PROGRESS

### Contributions 

David Kiernicki - Scraped the twitter data and wrote the code to scrape, create docker image and base flask, wrote half of the clustering code 

Jonathan Chang - Worked on correlation between seniment and polling (No longer being used), built out flask app, wrote code for saving models and cluster names