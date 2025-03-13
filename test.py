from app import app
from models import db, User



with app.app_context():
    Session = db.session()
    
    users = Session.query(User).order_by(User.id).limit(0).all()
    print(users)

    Session.commit()

print("Success!")