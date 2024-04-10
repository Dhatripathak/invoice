from flask import Flask, jsonify, request 
import subprocess 
from PyPDF2 import PdfReader, PdfWriter 
import os

app = Flask(__name__)

@app.route('/generate_certificate', methods=['GET']) 
def generate_certificate(): 
 try: # Signer details 
   signer_common_name = 'Your Name' 
   signer_organization = 'Your Organization' 
   signer_organization_unit = 'Your Organization Unit' 
   signer_locality = 'Your Locality' 
   signer_state = 'Your State' 
   signer_country = 'Your Country Code'

    # Generate private key
   subprocess.call(['openssl', 'genpkey', '-algorithm', 'RSA', '-out', 'private.key'])

    # Generate CSR
   subprocess.call(['openssl', 'req', '-new', '-key', 'private.key', '-out', 'csr.csr', '-subj', '/CN={}/O={}/OU={}/L={}/ST={}/C={}'.format(signer_common_name, signer_organization, signer_organization_unit, signer_locality,signer_state, signer_country)])

   
   subprocess.call(['openssl', 'x509', '-req', '-days', '365', '-in', 'csr.csr', '-signkey', 'private.key','-out', 'certificate.crt'])

   return jsonify({'message': 'Certificate generated successfully.'}), 200

 except Exception as e:
  return jsonify({'error': str(e)}), 500
@app.route('/sign__pdf', methods=['POST']) 
def sign__pdf(): 
 try: # Get the uploaded PDF file 
    pdf_file = request.files['file'] 
    pdf_data = pdf_file.read()

    # Load the PDF
    pdf = PdfReader(pdf_data)

    # Sign the PDF
    signature_image = 'signature.png'  # Path to the signature image
    output_pdf = 'signed_document.pdf'  # Path to the signed PDF

    for page in pdf.pages:
        page.merge_page(page)

    # Add the signature image to the first page
    signature_page = pdf.pages[0]
    signature_page.add_image(signature_image, x=100, y=100, width=200, height=50)

    # Save the signed PDF
    pdf_writer = PdfWriter()
    for page in pdf.pages:
        pdf_writer.add_page(page)

    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

    # Remove the temporary files
    os.remove('private.key')
    os.remove('csr.csr')
    os.remove('certificate.crt')

    return jsonify({'message': 'PDF signed successfully.'}), 200

 except Exception as e:
    return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)


