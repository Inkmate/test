from flask import Blueprint, jsonify, request
from docx import Document
import os

# Create a blueprint to define routes related to certificates
print_routes = Blueprint('print_routes', __name__)

# Directory where the .docx files are stored
UPLOAD_FOLDER = 'certificates'
print_routes.config = {'UPLOAD_FOLDER': UPLOAD_FOLDER}

# Helper function to extract text from a .docx file
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)

# Print route to serve the .docx content and log the print action
@print_routes.route("/print/<filename>", methods=["POST"])
def print_certificate(filename):
    file_path = os.path.join(print_routes.config['UPLOAD_FOLDER'], filename)

    # Check if the file exists
    if os.path.exists(file_path):
        # Extract the text content from the .docx file
        text = extract_text_from_docx(file_path)
        
        # Log the print action (you can save this to a log file or database if needed)
        print(f"Print action logged for {filename}")  # Simple logging

        # Return the text content as HTML for editing or displaying
        html_content = f"<div>{text}</div>"
        return jsonify({"message": "Print action logged and content served", "content": html_content})
    else:
        return jsonify({"error": "File not found"}), 404
