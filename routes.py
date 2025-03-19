from flask import render_template, request, session, redirect, url_for
from models import db, User, Subject

from app import app  # Import app after it is initialized

@app.route('/')
def home():
    if session.get('user_email'):
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if session.get('user_email'):
            return redirect(url_for('dashboard'))
        return render_template('register.html')
    elif request.method == "POST":
        user_name = request.form.get("name")
        user_email = request.form.get("email")
        user = User(name=user_name, email=user_email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get('user_email'):
            return redirect(url_for('dashboard'))
        return render_template('login.html')
    elif request.method == "POST":
        user_passowrd = request.form.get("name")
        user_email = request.form.get("email")
        user = db.session.get(User, user_email)
        if user:
            # user.password == user_passowrd
            session['user_email'] = user.email
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        return redirect(url_for('register'))
    
@app.route('/logout', methods=["GET"])
def logout():
    if session.get('user_email'):
        session['user_email'] = None
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    logged_in = session.get('user_email')
    if logged_in:
        user = db.session.get(User, session.get('user_email'))
        return render_template('user/dashboard.html')
    else:
        return redirect('/')
    
@app.route('/admin/dashboard')
def admin_dashboard():
    logged_in = session.get('user_email')
    if logged_in: user = db.session.get(User, session.get('user_email'))
    else: return redirect('/')

    if user.role == 'admin':
        return render_template('admin/dashboard.html')
    else:
        return "You are not allowed to this route! <a href='/'>Click here</a> to go dashboard"

@app.route('/subjects', methods=['GET', 'POST'])
def subjects():
    if request.method == 'GET':
        if request.args.get('update'): # user trying to update
            subject = db.session.get(Subject, request.args.get('subject_id'))
            return render_template('subjects.html', is_update=True, subject=subject)
        subjects = db.session.query(Subject).all()
        return render_template('subjects.html', subjects=subjects)
    elif request.method == 'POST':
        if request.form.get('delete'):
            subject_id = request.form.get('subject_id')
            subject = db.session.get(Subject, subject_id)
            db.session.delete(subject)
            db.session.commit()
            return redirect('/subjects')
        if request.form.get('update'):
            subject_id = request.form.get('subject_id')
            subject = db.session.get(Subject, subject_id)
            subject.name = request.form.get('name')
            subject.description = request.form.get('description')
            db.session.commit()
            return redirect('/subjects')
        name = request.form.get('name')
        description = request.form.get('description')
        subject = Subject(name=name, description=description)
        db.session.add(subject)
        db.session.commit()
        return redirect('/subjects')
    
@app.route('/subjects/<subject_id>')
def subject(subject_id):
    subject = db.session.get(Subject, subject_id)
    if subject:
        return render_template('subject.html', subject=subject)
    return "Subject Not found!"

@app.route('/exam')
def exam():
    return render_template('exam.html')