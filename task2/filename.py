from flask import Flask, request, jsonify
from PyPDF2 import PdfFileReader
from PIL import Image

app = Flask(__name__)

@app.route('/checkfile', methods=['POST'])
def check_file():
    file = request.files['file']
    try:
       
        pdf = PdfFileReader(file)
        if pdf.getNumPages() > 0:
           
            with open(file.filename, 'rb') as f:
                if f.read(5) != b'%PDF-':
                    return jsonify({'result': 'Corrupted PDF file'})
            return jsonify({'result': 'Valid PDF file'})
    except:
        pass

    try:
       
        img = Image.open(file)
        img.verify()
        if img.format in ['JPEG', 'PNG']:
            return jsonify({'result': f'{img.format} image'})
    except:
        pass

    return jsonify({'result': 'File is corrupt or not a PDF/JPEG/PNG'})

if __name__ == '__main__':
    app.run()
