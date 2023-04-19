import flask as fl
import os
import pymongo as pm

mongo_uri = os.environ['MONGO_URI']

app = fl.Flask(__name__, static_folder='static')
client = pm.MongoClient(mongo_uri)

@app.route('/')
def index():
    return fl.render_template("index.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)



