from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017/')
db = client['shop_database']
shops_collection = db['shops']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/seller', methods=['GET', 'POST'])
def seller():
    if request.method == 'POST':
        shop_name = request.form['shopName']
        shop = shops_collection.find_one({'name': shop_name})
        if shop:
            return redirect(url_for('add_content'))
        else:
            return redirect(url_for('add_shop'))
    return render_template('seller.html')

@app.route('/customer')
def customer():
    return render_template('customer.html')

@app.route('/add_content')
def add_content():
    return render_template('add_content.html')

@app.route('/add_shop')
def add_shop():
    return render_template('add_shop.html')

if __name__ == '__main__':
    app.run(debug=True)
