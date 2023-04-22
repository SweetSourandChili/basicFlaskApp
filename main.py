import flask as fl
import pymongo as pm
import certifi
import os
import secrets

mongo_uri = os.environ['MONGO_URI']

app = fl.Flask(__name__, static_folder='static')
app.secret_key = secrets.token_hex(16)
client = pm.MongoClient(mongo_uri, ssl_ca_certs=certifi.where())

db = client['webData']
users = db['userData']


@app.route('/')
def index():
    return fl.render_template("index.html", username=fl.session.get('username', None))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if fl.request.method == 'GET':
        return fl.render_template('login.html')

    loggedIn = fl.request.form.get('loggedIn')
    if loggedIn:
        fl.session.pop('username', None)
        return fl.jsonify({'success': True, 'message': 'Logged out.', 'logged_in': False}), 200

    username = fl.request.form['username']
    password = fl.request.form['password']

    print(fl.request.form.get("admin"))
    if fl.request.form.get("admin"):
        user = users.find_one({"username": username, "admin": True})
    else:
        user = users.find_one({"username": username, "admin": False})

    if user is None:
        return fl.jsonify({'success': False, 'message': 'This user is not registered!'}), 405
    else:
        if user["password"] == password:
            fl.session['username'] = username
            return fl.jsonify({'success': True, 'message': 'Successful'.format(username)}), 200
        else:
            return fl.jsonify({'success': False, 'message': 'Wrong password!'.format(username)}), 406


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if fl.request.method == 'GET':
        return fl.render_template("admin.html")


@app.route('/user', methods=['POST'])
def user():
    username = fl.request.form.get('username')
    password = fl.request.form.get('password')
    add = fl.request.form.get('add')

    if add == 'True':
        # Check if the user already exists in the database
        user_instance = users.find_one({"username": username})
        if user_instance:
            return fl.jsonify({'success': False, 'message': 'This username already exists!'}), 405
        elif username == "" or password == "":
            return fl.jsonify({'success': False, 'message': 'Empty fields!'}), 405

        users.insert_one({
            'username': username,
            'password': password,
            'avgRating': None,
            'reviews': [],
            'admin': False
        })

        return fl.jsonify({'success': True, 'message': 'User created successfully!'}), 200

    else:
        result = users.delete_one({'username': username})
        if result.deleted_count == 1:
            return fl.jsonify({'success': True, 'message': 'User deleted successfully!'}), 200
        else:
            return fl.jsonify({'success': False, 'message': 'User not found!'}), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
