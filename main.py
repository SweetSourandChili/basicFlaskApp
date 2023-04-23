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
reviews = db['reviews']

item_types = {0: clothing, 1: compComponents, 2: monitors, 3: snacks}


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
            "price": int(fl.request.form.get('price')),
            "currency": "$",
            "seller": fl.request.form.get('seller'),
            "image": fl.request.form.get('image_link'),
            "size": fl.request.form.get('size'),
            "colour": fl.request.form.get('colour'),
            "spec": fl.request.form.get('spec'),
            "rating": "No ratings.",
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
            result = clothing.delete_one({'name': fl.request.form.get('name')})
            if result.deleted_count == 1:
                return fl.jsonify({'success': True, 'message': 'Item(Clothing) deleted successfully!'}), 200
            else:
                return fl.jsonify({'success': False, 'message': 'Item not found!'}), 404

        elif type == 1:
            result = compComponents.delete_one({'name': fl.request.form.get('name')})
            if result.deleted_count == 1:
                return fl.jsonify(
                    {'success': True, 'message': 'Item(Computer Components) deleted successfully!'}), 200
            else:
                return fl.jsonify({'success': False, 'message': 'Item not found!'}), 404

        elif type == 2:
            result = monitors.delete_one({'name': fl.request.form.get('name')})
            if result.deleted_count == 1:
                return fl.jsonify({'success': True, 'message': 'Item(Monitors) deleted successfully!'}), 200
            else:
                return fl.jsonify({'success': False, 'message': 'Item not found!'}), 404

        elif type == 3:
            result = snacks.delete_one({'name': fl.request.form.get('name')})
            if result.deleted_count == 1:
                return fl.jsonify({'success': True, 'message': 'Item(Snacks) deleted successfully!'}), 200
            else:
                return fl.jsonify({'success': False, 'message': 'Item not found!'}), 404
        else:
            return fl.jsonify({'success': False, 'message': 'Wrong type value!'}), 405


@app.route('/list', methods=['POST'])
def listItems():
    onload = fl.request.form.get('onload')
    if onload == 'True':
        documents = list()
        for value in item_types.values():
            documents += list(value.find({}, {'_id': 0}))
    else:
        filter_num = int(fl.request.form.get('filter_type'))
        type = int(fl.request.form.get('item_type'))
        if filter_num == -1:
            documents = list(item_types.get(type).find({}, {'_id': 0}))
        elif filter_num == 0:  # Highest Rating
            documents = list(item_types.get(type).find({}, {'_id': 0}).sort('rating', -1))
        elif filter_num == 1:  # Lowest Rating
            documents = list(item_types.get(type).find({}, {'_id': 0}).sort('rating', 1))
        elif filter_num == 2:  # Cheap to Expensive
            documents = list(item_types.get(type).find({}, {'_id': 0}).sort('price', 1))
        elif filter_num == 3:  # Expensive to Cheap
            documents = list(item_types.get(type).find({}, {'_id': 0}).sort('price', -1))
        else:
            documents = list()

    for document in documents:
        list_reviews = list()
        review_ids = document["reviews"]
        for id in review_ids:
            res = reviews.find_one({"_id": id})
            username = users.find_one({"_id": res["user_id"]})["username"]
            list_reviews.append({"username": username, "inner": res["review"], "rating": res["rating"]})
        document["reviews"] = list_reviews

    return fl.jsonify(documents), 200


@app.route('/review', methods=['POST'])
def postItems():
    username = fl.session.get('username', None)
    if username:
        type = int(fl.request.form.get('type'))
        item_name = fl.request.form.get('item_name')
        review = fl.request.form.get('review')
        rating = int(fl.request.form.get('rating'))

        curr_user = users.find_one({"username": username})
        curr_item = item_types.get(type).find_one({"name": item_name})

        # check if the user has a review before
        user_reviews = curr_user.get("reviews", [])
        curr_review_id = None
        for r in user_reviews:
            is_found = item_types.get(type).find_one({"name": item_name, "reviews": {"$in": [r]}})
            if is_found is not None:
                curr_review_id = r
                break

        if curr_review_id:
            if review != "":
                query = {"$set": {"rating": rating, "review": review}}
            else:
                query = {"$set": {"rating": rating}}
            review_result = reviews.update_one({"_id": curr_review_id}, query)
            if review_result.modified_count > 0:
                avg_rating = find_avg_rating(curr_item["name"], type)
                item_types.get(type).update_one({"name": item_name}, {"$set": {"rating": avg_rating}})
                return fl.jsonify({'success': True, 'message': 'Review is updated.'}), 200
            else:
                return fl.jsonify({'success': False, 'message': 'Review can not be updated.'}), 405
        else:
            new_review = {
                "user_id": curr_user["_id"],
                "rating": rating,
                "review": review
            }
            result = reviews.insert_one(new_review)
            review_id = result.inserted_id
            if not result.acknowledged:
                return fl.jsonify({'success': False, 'message': 'Can not saved to the database!'}), 405
            item_types.get(type).find_one({"name": item_name})
            user_result = users.update_one({"username": username}, {"$push": {"reviews": review_id}})
            review_result = item_types.get(type).update_one({"_id": curr_item["_id"]},
                                                            {"$push": {"reviews": review_id}})

            if user_result.modified_count > 0 and review_result.modified_count > 0:
                avg_rating = find_avg_rating(curr_item["name"], type)
                item_types.get(type).update_one({"name": item_name}, {"$set": {"rating": avg_rating}})
                return fl.jsonify({'success': True, 'message': 'Review is saved.'}), 200
            else:
                return fl.jsonify({'success': False, 'message': 'Review can not be updated!'}), 405

    else:
        return fl.jsonify({'success': False, 'message': 'User not logged in!'}), 405


def find_avg_rating(item_name, type):
    item_reviews_ids = item_types.get(type).find_one({"name": item_name})["reviews"]
    list_ratings = list()
    for id in item_reviews_ids:
        list_ratings.append(reviews.find_one({"_id": id})["rating"])

    if len(list_ratings) == 0:
        return 0
    return sum(list_ratings) / len(list_ratings)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
