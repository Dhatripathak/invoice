from flask import Flask, request
from pymongo import MongoClient
import json

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']

@app.route('/adduser', methods=['POST'])
def add_user():
    data = json.loads(request.data)
    name = data ['name']
    mobile = data['mobile']
    user_id = data['id']
    user = {'name': name, 'mobile': mobile, 'id': user_id}
    result = db.users.insert_one(user)
    return {'message': 'User added successfully', 'id': str(result.inserted_id)}

@app.route('/getuser/<id>', methods=['GET'])
def get_user(id):
    user = db.users.find_one({'id': id})
    if user:
        return {'name': user['name'], 'mobile': user['mobile'], 'id': user['id']}
    else:
        return {'message': 'User not found'}

if __name__ == '__main__':
    app.run(debug=True)
