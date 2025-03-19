from flask import Flask
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "MAD1Bootcamp"

db.init_app(app)

with app.app_context():
    db.create_all()
    
    # adding the admin
    admin_name = 'Admin'
    admin_email = 'admin@qmaster.com'
    if not db.session.get(User, admin_email):
        admin = User(name=admin_name, email=admin_email, role='admin')
        db.session.add(admin)
        db.session.commit()
        print('Created admin')

from routes import *  # Import routes after initializing db

if __name__ == '__main__':
    app.run(debug=True)