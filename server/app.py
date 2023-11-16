from flask import Flask, request, jsonify, send_from_directory
import os

# Import other necessary modules and functions
from ner import perform_ner
from database import query_database
from pdf_handler import handle_pdf

app = Flask(__name__)

# Set your configuration directly here
# app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'pdfs/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['DEBUG'] = True  # Set to False in production

# Serve the React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Endpoint to upload PDFs
@app.route('/upload', methods=['POST'])
def upload_pdf():
    # Handle file upload and save to 'pdfs' directory
    file = request.files['file']
    save_path = os.path.join('pdfs', file.filename)
    file.save(save_path)
    return jsonify({'message': 'File uploaded successfully!'})

# Endpoint to perform NER on a selected PDF
@app.route('/ner', methods=['POST'])
def perform_ner():
    # Extract named entities from the PDF
    pdf_path = request.json['pdf_path']
    entities = perform_ner(pdf_path)
    return jsonify(entities)

# Endpoint to get entity linking data from the database
@app.route('/entity-linking', methods=['POST'])
def get_entity_linking():
    # Get entity linking data from the database
    entity_name = request.json['entity_name']
    linking_data = query_database(entity_name)
    return jsonify(linking_data)

if __name__ == '__main__':
    app.run(debug=True)
