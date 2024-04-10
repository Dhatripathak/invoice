from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from PIL import Image
import magic
import os
from io import BytesIO



app = Flask(__name__)
@app.route('/checkfile', methods=['POST'])
def check_file():
    file = request.files['file']

    try:        
        with open(file.filename, 'rb') as f:
            if f.read(5) != b'%PDF-':
                return jsonify({'result': 'Corrupt PDF file'})

       
        buffer = BytesIO()
        buffer.write(file.read())
        file_type = magic.from_buffer(buffer.getvalue(), mime=True)
        file_ext = os.path.splitext(file.filename)[1]

      
        try:
            pdf = PdfReader(file.stream)
            if len(pdf.pages) > 0:
                if file_type == 'application/pdf' and file_ext == '.pdf':
                    return jsonify({'result': 'PDF file'})
        except:
            pass

       
        try:
            img = Image.open(file.stream)
            img.verify()
            if img.format in ['JPEG']:
                if 'jpeg' in file_type and file_ext == '.jpeg': 
                    return jsonify({'result': f'{img.format} image'})
        except:
            pass
        
       
        try:
            img = Image.open(file.stream)
            img.verify()
            if img.format in ['PNG']:
                if 'png' in file_type and file_ext == '.png':
                    return jsonify({'result': f'{img.format} image'})
        except:
            pass
        
        return jsonify({'result': 'File is not a PDF/JPEG/PNG'})

    except:
        return jsonify({'result': 'File is corrupt or cannot be opened'})  
if __name__ == '__main__':
    app.run()