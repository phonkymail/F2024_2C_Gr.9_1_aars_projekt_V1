import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from werkzeug.utils import secure_filename

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {
    'users_db': 'sqlite:///users.db',
    'login_db': 'sqlite:///login.db'
}
app.config['UPLOAD_FOLDER'] = '/home/rav/Desktop/smartlock/main/upload'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['MAX_CONTENT_PATH'] = 1024 * 1024 * 10

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'user'
    __bind_key__ = 'users_db'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

class Worker(db.Model):
    __tablename__ = 'worker'
    __bind_key__ = 'users_db'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Intruder(db.Model):
    __tablename__ = 'intruder'
    __bind_key__ = 'users_db'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    photo = db.Column(db.String(100), nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    __bind_key__ = 'login_db'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

# Create the databases
with app.app_context():
    db.create_all()

# Function to handle image upload
def process_image_upload(photo):
    if photo:
        filename = secure_filename(photo.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(file_path)
        return filename
    return None

# Route to handle form submission
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        photo = request.files['photo']

        if photo:
            filename = process_image_upload(photo)
            if filename:
                new_user = User(first_name=first_name, last_name=last_name, photo=filename)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('admin'))

    users = User.query.all()
    return render_template('admin.html', users=users)

# Route to serve image from the upload folder
@app.route('/home/rav/Desktop/smartlock/main/upload/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route to delete a user entry
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], user.photo))
    except:
        pass
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/')
def index():
    return render_template('index.html')

# Route to query Worker table
@app.route('/workers')
def view_workers():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    workers = Worker.query.all()
    return render_template('workers.html', workers=workers)

# Route to query Intruder table
@app.route('/intruders')
def view_intruders():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    intruders = Intruder.query.all()
    return render_template('intruders.html', intruders=intruders)

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Admin.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
    return render_template('login.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# Route for About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for Services page
@app.route('/services')
def services():
    return render_template('services.html')

# Route for Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

