from flask import Flask
import os
import ssl
from pymongo import MongoClient

# Retrieve the MongoDB Atlas URI from the environment variables
mongo_uri = os.environ['MONGO_URI']

app = Flask(__name__)
client = MongoClient(mongo_uri)


@app.route('/')
def hello_world():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run()



