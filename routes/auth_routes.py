from flask import Blueprint, request, redirect, url_for, session, render_template
import csv
import os

auth_bp = Blueprint("auth", __name__)

USER_CREDENTIALS = {"admin": "password123"}  # Default user

CSV_FILE = "users.csv"

# Load users from CSV file
if os.path.exists(CSV_FILE):
    with open(CSV_FILE, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                username, password = row
                USER_CREDENTIALS[username] = password

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard.dashboard"))
        return "Invalid credentials", 401

    # Renders your single-page login/register form
    return render_template("login.html")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in USER_CREDENTIALS:
        return "Username already exists", 409

    # Store the new user
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

    USER_CREDENTIALS[username] = password
    return redirect(url_for("auth.login"))

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))
