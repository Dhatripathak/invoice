from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/hello', methods=['POST'])
def hello():
   
    name = request.form.get('name', 'World')
    message = f'Hello, {name}!'
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run()
