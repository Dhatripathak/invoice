from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['shop_database']
shops_collection = db['shops']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_shop', methods=['POST'])
def add_shop():
    if request.method == 'POST':
        shop_name = request.form['shopName']
        billing_address = request.form['billingAddress']
        shipping_address = request.form['shippingAddress']
        registration_no = request.form['registrationNo']
        
        # Insert data into MongoDB for the specified shop
        shop_data = {
            'name': shop_name,
            'billing_address': billing_address,
            'shipping_address': shipping_address,
            'registration_no': registration_no
        }
        shops_collection.insert_one(shop_data)
        
        return 'Shop added successfully!'
    else:
        return 'Error in form submission'

if __name__ == '__main__':
    app.run(debug=True)
