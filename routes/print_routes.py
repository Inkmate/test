from flask import Blueprint, request, send_file, jsonify
from docxtpl import DocxTemplate
import os
from io import BytesIO
import traceback

print_bp = Blueprint("print", __name__)
UPLOAD_FOLDER = 'certificates'
print_bp.config = {'UPLOAD_FOLDER': UPLOAD_FOLDER}

@print_bp.route("/print/<filename>", methods=["POST"])
def print_certificate(filename):
    file_path = os.path.join(print_bp.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        data = request.get_json()

        # Prepare context from frontend form
        context = {
            'name': data.get('employeeName', ''),
            'position': data.get('position', ''),
            'school': data.get('school', ''),
            'first_day': data.get('firstDay', ''),
            'salary': data.get('basicSalary', ''),
            'promotion_date': data.get('promotionDate', ''),
            'date_today': data.get('dateToday', ''),
        }

        # Load and render the template
        doc = DocxTemplate(file_path)
        doc.render(context)

        output_stream = BytesIO()
        doc.save(output_stream)
        output_stream.seek(0)

        return send_file(
            output_stream,
            as_attachment=True,
            download_name="Generated-Certificate.docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        traceback.print_exc() 
        return jsonify({"error": f"Error processing document: {str(e)}"}), 500





# from flask import Blueprint, request, jsonify
# from docx import Document
# import os
# from utils import update_log
# import traceback

# print_bp = Blueprint("print", __name__)

# # Directory where the .docx files are stored
# UPLOAD_FOLDER = 'certificates'
# print_bp.config = {'UPLOAD_FOLDER': UPLOAD_FOLDER}

# # Helper function to extract text from a .docx file
# def extract_text_from_docx(file_path):
#     doc = Document(file_path)
#     html = ""
#     for para in doc.paragraphs:
#         p_html = "<p>"
#         for run in para.runs:
#             text = run.text
#             if run.bold:
#                 text = f"<strong>{text}</strong>"
#             if run.italic:
#                 text = f"<em>{text}</em>"
#             p_html += text
#         p_html += "</p>\n"
#         html += p_html
#     return html

# # Print route to serve the .docx content and log the print action
# @print_bp.route("/print/<filename>", methods=["POST"])
# def print_certificate(filename):
#     file_path = os.path.join(print_bp.config['UPLOAD_FOLDER'], filename)

#     if os.path.exists(file_path):
#         html_content = extract_text_from_docx(file_path)
#         print(f"Print action logged for {filename}")
#         return jsonify({"message": "Print action logged and content served", "content": html_content})
#     else:
#         return jsonify({"error": "File not found"}), 404
