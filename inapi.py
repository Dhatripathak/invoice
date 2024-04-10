from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file_type = file.content_type
        file_ext = os.path.splitext(file.filename)[1]
        print(file_type)
        print(file_ext)
        if file_type == 'application/pdf' and file_ext == '.pdf':
           return "Valid file format"
        if 'jpeg' in file_type and file_ext == '.jpeg':
            return "Valid file format"
        if 'png' in file_type and file_ext == '.png':           
            return "Valid file format"
      
    return "Invalid file format"

if __name__ == '__main__':
    app.run()
    
    