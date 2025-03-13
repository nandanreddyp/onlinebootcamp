from flask import Flask
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

with app.app_context():
    db.create_all()

from routes import *  # Import routes after initializing db

if __name__ == '__main__':
    app.run(debug=True)