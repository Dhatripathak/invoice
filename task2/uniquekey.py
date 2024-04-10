from flask import Flask, request, jsonify
from pymongo import MongoClient
import re

app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
users_collection = db['users']


mobile_regex = re.compile(r'^\d{10}$')

@app.route('/users', methods=['POST'])
def add_user():
   
    mobile = request.json.get('mobile')
    details = request.json.get('details')

   
    if not mobile_regex.match(mobile):
        return jsonify({'error': 'Invalid mobile number format'}), 400

   
    result = users_collection.insert_one({'mobile': mobile, 'details': details})
    if not result.inserted_id:
        return jsonify({'error': 'Failed to add user'}), 500

    return jsonify({'message': 'User added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
