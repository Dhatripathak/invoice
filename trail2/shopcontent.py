from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['shop_database']
collection = db['shops']

@app.route('/')
def index():
    return render_template('shop_input.html')

@app.route('/check_shop', methods=['POST'])
def check_shop():
    if request.method == 'POST':
        shop_name = request.form['shopName']
        shop = collection.find_one({'name': shop_name})
        if shop:
            return jsonify({'exists': True})
        else:
            return jsonify({'exists': False})

@app.route('/add_shop_details', methods=['POST'])
def add_shop_details():
    if request.method == 'POST':
        shop_name = request.form['shopName']
        shop_address = request.form['shopAddress']
        gst_number = request.form['gstNumber']
        
        # Insert data into MongoDB for the specified shop
        shop_data = {
            'name': shop_name,
            'address': shop_address,
            'gst_number': gst_number
        }
        collection.insert_one(shop_data)
        
        return 'Shop details added successfully!'
    else:
        return 'Error in form submission'

if __name__ == '__main__':
    app.run(debug=True)
