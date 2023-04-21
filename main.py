import flask as fl
import pymongo as pm
import certifi
import os

mongo_uri = os.environ['MONGO_URI']

app = fl.Flask(__name__, static_folder='static')
client = pm.MongoClient(mongo_uri, ssl_ca_certs=certifi.where())
db = client['webData']

users = db['userData']

@app.route('/')
def index():
    return fl.render_template("index.html")


@app.route('/loginUser', methods=['POST'])
def loginUser():
    username = fl.request.form['username']
    password = fl.request.form['password']
    # TODO: check to send token here
    user = users.find_one({"username": username, "admin": False})
    if user is None:
        return fl.jsonify({'success': True, 'message': 'This user is not registered!'}), 405
    else:
        if user["password"] == password:
            return fl.redirect("dashboard.html")
        else:
            return fl.jsonify({'success': True, 'message': 'Wrong password!'.format(username)}), 406

@app.route('/loginAdmin', methods=['POST'])
def loginAdmin():
    username = fl.request.form['username']
    password = fl.request.form['password']
    user = users.find_one({"username": username, "admin": True})
    if user is None:
        return fl.jsonify({'success': True, 'message': 'This admin is not registered!'}), 405
    else:
        if user["password"] == password:
            return fl.redirect("admin.html")
        else:
            return fl.jsonify({'success': True, 'message': 'Wrong password!'}), 406


@app.route('/getData', methods=['POST'])
def getData():
    try:
        db.command('ping')
        return fl.jsonify({'success': True, 'message': 'Login successful'}), 200
    except Exception as e:
        print(str(e))
        return fl.jsonify({'success': False, 'message': 'Login successful'}), 505


@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    return fl.redirect(fl.url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    print("here")
    return fl.render_template('dashboard.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
