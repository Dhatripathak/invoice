from flask import Flask, request, jsonify
from PyPDF2 import PdfFileReader

app = Flask(__name__)

@app.route('/check_pdf', methods=['POST'])
def check_pdf():
    file = request.files['pdf']
    try:
        pdf = PdfFileReader(file)
        if pdf.getNumPages() > 0:
            if pdf.getPage(0).extractText().strip():
                return jsonify({'result': 'PDF contains text'})
            else:
                return jsonify({'result': 'PDF does not contain text'})
        else:
            return jsonify({'result': 'PDF is empty'})
    except:
        return jsonify({'result': 'Invalid or corrupted PDF file'})

if __name__ == '__main__':
    app.run()
