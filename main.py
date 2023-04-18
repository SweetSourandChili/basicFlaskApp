from flask import Flask, render_template
import os
import ssl
from pymongo import MongoClient

mongo_uri = os.environ['MONGO_URI']

app = Flask(__name__, static_folder='static')
client = MongoClient(mongo_uri)

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)



