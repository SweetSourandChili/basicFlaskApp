from flask import Flask
import os
from pymongo import MongoClient
app = Flask(__name__)


client = MongoClient(os.environ['MONGO_URI'])
db = client['your-database-name']

@app.route('/')
def hello_world():
    return 'Hello, World!'



