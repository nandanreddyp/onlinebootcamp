from flask import render_template, request, session, redirect, url_for
from models import db, User

dbSession = db.session  # Correct usage

from app import app  # Import app after it is initialized

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        user_name = request.form.get("name")
        user_email = request.form.get("email")
        user = User(name=user_name, email=user_email)
        dbSession.add(user)
        dbSession.commit()
        return redirect(url_for('dashboard'))

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return 'Dashboard'