from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app import Admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'login_db': 'sqlite:///login.db'
}
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

def create_admin(username, password):
    with app.app_context():
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 
        new_admin = Admin(username=username, password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()
        print('Administrator created successfully')

if __name__ == '__main__':
    username = input('Enter username for admin: ')
    password = input('Enter password for admin: ')
    create_admin(username, password)
