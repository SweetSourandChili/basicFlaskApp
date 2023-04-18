from flask import Flask, render_template
import os
import ssl
from pymongo import MongoClient

# Retrieve the MongoDB Atlas URI from the environment variables
mongo_uri = os.environ['MONGO_URI']

app = Flask(__name__)
client = MongoClient(mongo_uri)

@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)



