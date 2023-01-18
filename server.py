from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from recommender import *

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return jsonify({"message": "server is live"})

@app.route("/title", methods=['POST'])
def title():
    content = request.get_json()
    print(content)
    df = recommend_from_title(content['courseId'], int(content['queryNumber']))
    return pd.DataFrame.to_json(df)

@app.route("/keyword", methods=['POST'])
def keyword():
    try:
        content = request.get_json()
        print(content)
        df = recommend_from_keyword(content['keyword'], int(content['number']))
        return pd.DataFrame.to_json(df, orient='records')
    except ValueError as e:
        return ([{"message": "error"}])