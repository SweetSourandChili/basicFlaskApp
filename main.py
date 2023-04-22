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

clothing = db['clothing']
compComponents = db['compComponents']
monitors = db['monitors']
snacks = db['snacks']


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

    if fl.request.form.get("admin") == 'True':
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
    add = fl.request.form.get('add')

    if add == 'True':
        password = fl.request.form.get('password')
        # Check if the user already exists in the database
        user_instance = users.find_one({"username": username})
        if user_instance:
            return fl.jsonify({'success': False, 'message': 'This username already exists!'}), 405
        elif username == "" or password == "":
            return fl.jsonify({'success': False, 'message': 'Empty fields!'}), 405

        result = users.insert_one({
            'username': username,
            'password': password,
            'avgRating': None,
            'reviews': [],
            'admin': False
        })
        if result.acknowledged:
            return fl.jsonify({'success': True, 'message': 'User created successfully.'}), 200
        else:
            return fl.jsonify({'success': False, 'message': 'Can not reach the server!'}), 405


    else:
        result = users.delete_one({'username': username})
        if result.deleted_count == 1:
            return fl.jsonify({'success': True, 'message': 'User deleted successfully!'}), 200
        else:
            return fl.jsonify({'success': False, 'message': 'User not found!'}), 404


@app.route('/item', methods=['POST'])
def item():
    add = fl.request.form.get('add')
    type = int(fl.request.form.get('item_type'))
    if add == 'True':
        query = {
            "name": fl.request.form.get('name'),
            "description": fl.request.form.get('description'),
            "price": fl.request.form.get('price'),
            "currency": "$",
            "seller": fl.request.form.get('seller'),
            "image": fl.request.form.get('image_link'),
            "size": fl.request.form.get('size'),
            "colour": fl.request.form.get('colour'),
            "spec": fl.request.form.get('spec'),
            "rating": None,
            "reviews": []
        }
        if type == 0:
            check_old = clothing.find_one({'name': fl.request.form.get('name')})
            if check_old:
                return fl.jsonify({'success': False, 'message': 'There is a item with the same name!'}), 405
            else:
                result = clothing.insert_one(query)

        elif type == 1:
            check_old = compComponents.find_one({'name': fl.request.form.get('name')})
            if check_old:
                return fl.jsonify({'success': False, 'message': 'There is a item with the same name!'}), 405
            else:
                result = compComponents.insert_one(query)

        elif type == 2:
            check_old = monitors.find_one({'name': fl.request.form.get('name')})
            if check_old:
                return fl.jsonify({'success': False, 'message': 'There is a item with the same name!'}), 405
            else:
                result = monitors.insert_one(query)

        elif type == 3:
            check_old = snacks.find_one({'name': fl.request.form.get('name')})
            if check_old:
                return fl.jsonify({'success': False, 'message': 'There is a item with the same name!'}), 405
            else:
                result = snacks.insert_one(query)

        else:
            return fl.jsonify({'success': False, 'message': 'Wrong type value!'}), 405

        if result.acknowledged:
            return fl.jsonify({'success': True, 'message': 'Item added successfully.'}), 200
        else:
            return fl.jsonify({'success': False, 'message': 'Can not reach the server!'}), 405

    else:
        if type == 0:
            check_old = clothing.find_one({'name': fl.request.form.get('name')})
            if check_old:
                result = clothing.delete_one({'name': fl.request.form.get('name')})
                if result.deleted_count == 1:
                    return fl.jsonify({'success': True, 'message': 'Item(Clothing) deleted successfully!'}), 200
                else:
                    return fl.jsonify({'success': False, 'message': 'Item not found!'}), 404

        if type == 1:
            check_old = compComponents.find_one({'name': fl.request.form.get('name')})
            if check_old:
                result = compComponents.delete_one({'name': fl.request.form.get('name')})
                if result.deleted_count == 1:
                    return fl.jsonify({'success': True, 'message': 'Item(Computer Components) deleted successfully!'}), 200
                else:
                    return fl.jsonify({'success': False, 'message': 'Item not found!'}), 404

        if type == 2:
            check_old = monitors.find_one({'name': fl.request.form.get('name')})
            if check_old:
                result = monitors.delete_one({'name': fl.request.form.get('name')})
                if result.deleted_count == 1:
                    return fl.jsonify({'success': True, 'message': 'Item(Monitors) deleted successfully!'}), 200
                else:
                    return fl.jsonify({'success': False, 'message': 'Item not found!'}), 404

        if type == 3:
            check_old = snacks.find_one({'name': fl.request.form.get('name')})
            if check_old:
                result = snacks.delete_one({'name': fl.request.form.get('name')})
                if result.deleted_count == 1:
                    return fl.jsonify({'success': True, 'message': 'Item(Snacks) deleted successfully!'}), 200
                else:
                    return fl.jsonify({'success': False, 'message': 'Item not found!'}), 404
        else:
            return fl.jsonify({'success': False, 'message': 'Wrong type value!'}), 405


@app.route('/list', methods=['POST'])
def listItems():
    type = int(fl.request.form.get('item_type'))
    if type == 0:
        documents = list(clothing.find({}, {'_id': 0}))
    elif type == 1:
        documents = list(compComponents.find({}, {'_id': 0}))
    elif type == 2:
        documents = list(monitors.find({}, {'_id': 0}))
    elif type == 3:
        documents = list(snacks.find({}, {'_id': 0}))
    else:
        documents = list()

    return fl.jsonify(documents), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
