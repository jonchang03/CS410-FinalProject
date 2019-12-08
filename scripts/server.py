import os
from flask import Flask, jsonify, request

import json
from prediction import make_prediction, return_features


HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def flask_app():
    app = Flask(__name__)


    @app.route('/', methods=['GET'])
    def server_is_up():
        # print("success")
        return 'server is up'

    @app.route('/predict_cluster', methods=['POST'])
    def start():
        to_predict = request.json

        # print(to_predict)
        pred = make_prediction(to_predict)
        return jsonify({"Predicted Clusters" : pred})
    
    @app.route('/get_cluster_titles', methods=['GET'])
    def get_titles():
        with open('models/cluster_labels.json', 'r') as json_file:
            data = json.load(json_file)
        titles = data['cluster_titles']
        for i in titles.keys(): 
            if titles[i] == "":
                titles[i] = i
        return jsonify({"Cluster Titles" : titles})

    @app.route('/get_cluster_features', methods=['GET'])
    def get_features():
        with open('models/cluster_labels.json', 'r') as json_file:
            data = json.load(json_file)
        titles = data['cluster_titles']
        features = return_features() 
        final_features = {}
        for t in features.keys() :
            fts = features[t]
            final_features[t] = fts
        return jsonify({"Cluster Features" : final_features})
    
    @app.route('/label_clusters', methods=['POST'])
    def label_clusters():
        labels = request.json
        with open('models/cluster_labels.json', 'r') as json_file:
            data = json.load(json_file)

        titles = data['cluster_titles']
        for k in labels.keys() : 
            titles[k] = labels[k]
        data['cluster_titles'] = titles
        with open('models/cluster_labels.json', 'w') as json_file:
            json.dump(data, json_file)
        return "Cluster Titles Updated"

    return app


if __name__ == '__main__':
    app = flask_app()
    app.run(debug=True, host='0.0.0.0')


