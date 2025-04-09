import os
from flask import Blueprint, session, redirect, url_for, render_template, send_file
from utils import extract_text_from_docx, update_log

dashboard_bp = Blueprint("dashboard", __name__)
CERTIFICATE_FOLDER = "certificates"

@dashboard_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    certificates = [f for f in os.listdir(CERTIFICATE_FOLDER) if f.endswith(".docx")]
    return render_template("dashboard.html", certificates=certificates)

@dashboard_bp.route("/generate/<filename>")
def generate_certificate(filename):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    filepath = os.path.join(CERTIFICATE_FOLDER, filename)
    content = extract_text_from_docx(filepath) if os.path.exists(filepath) else "File not found."
    return render_template("index.html", content=content, filename=filename)

@dashboard_bp.route("/download/<filename>")
def download_certificate(filename):
    update_log(filename, "download")
    return send_file(os.path.join(CERTIFICATE_FOLDER, filename), as_attachment=True)
