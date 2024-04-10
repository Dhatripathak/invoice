from flask import Flask, request
import pymongo

db = 'mydatabase'
uri = 'mongodb://localhost:27017/' + db
collection_name_users = 'users'
accounts_mongo_connection = pymongo.MongoClient(uri)[db]
users_collection = accounts_mongo_connection[collection_name_users]


app = Flask(__name__)


@app.route('/demo', methods=['GET'])
def demo():
    return {'status':'Done'}


@app.route('/users_list/<dlid>', methods=['POST'])
def users_list(dlid):
    where = {'dlid': dlid} 
    
    
    print(where)
    exit()
    data = users_collection.find(where, projection={'_id': False})
    # print(*data)
    # exit()
    for x in data:
        # print(type(x))
        # exit()
        return {'status':'success','data':x}
    
    return {'status':'error','error_description':'No data found!'}   

@app.route('/add_users_record', methods=['POST'])
def add_users_record():
    try:
        aadhaar = request.values.get('aadhaar')
        name = request.values.get('name')
        gender = request.values.get('gender')
        mobile = request.values.get('mobile')
        if aadhaar is None:
            return {'status':'error','error_description':'aadhaar data not found!'}
        
        
        data = {}
        print(data)
        data['aadhaar'] = aadhaar
        
        data['name'] = name
        data['gender'] = gender
        data['mobile_no'] = mobile
        
        res = users_collection.insert_one(data)
        if res.acknowledged is True and res.inserted_id is not None:
            return {'status': 'success', 'msg': 'Data Inserted'}
        else:
            return {'status': 'error', 'msg': 'Some technical error occurred.'}
    except Exception as e:
        return {'status': 'error', 'msg': str(e)}

@app.route('/delete', methods=['POST'])
def delete():
    try:
        aadhaar = request.values.get('aadhaar')
        
        if aadhaar is None:
            return {'status':'error','error_description':'aadhaar data found!'}
        filter = {'aadhaar':aadhaar}
                        
        res = users_collection.find_one_and_delete(filter)
                
        if res.acknowledged is True and res.inserted_id is not None:
            return {'status': 'success', 'msg': 'Data Inserted'}
        else:
            return {'status': 'error', 'msg': 'Some technical error occurred.'}
    except Exception as e:
        return {'status': 'error', 'msg': str(e)}
    

app.run(host='0.0.0.0', port=5000, debug=True)