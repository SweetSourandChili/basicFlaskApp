import flask as fl
import os
import pymongo as pm

mongo_uri = os.environ['MONGO_URI']

app = fl.Flask(__name__, static_folder='static')
client = pm.MongoClient(mongo_uri)
db = client['webData']


@app.route('/')
def index():
    return fl.render_template("index.html")


@app.route('/loginUser', methods=['POST'])
def loginUser():
    username = fl.request.form['username']
    password = fl.request.form['password']
    # TODO: check to send token here
    return fl.jsonify({'success': True, 'message': 'Login successful'}), 200


@app.route('/loginAdmin', methods=['POST'])
def loginAdmin():
    username = fl.request.form['username']
    password = fl.request.form['password']
    # TODO: check to send token here
    return fl.jsonify({'success': True, 'message': 'Login successful'}), 200


@app.route('/getData', methods=['POST'])
def getData():
    print("here")
    try:
        db.command('ping')
        print("here")
        return fl.jsonify({'success': True, 'message': 'Login successful'}), 200
    except Exception as e:
        print(str(e))
        return fl.jsonify({'success': False, 'message': 'Login successful'}), 505


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
