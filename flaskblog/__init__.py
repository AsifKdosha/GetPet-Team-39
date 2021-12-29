from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

with app.app_context():
    from .models import User, Post
    db.create_all()
    if User.query.filter_by(email="admin@admin.com").count() == 0:
        hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
        default_user = User(name='admin', email="admin@admin.com", password=hashed_password, is_admin=True)
        db.session.add(default_user)
        db.session.commit()

from flaskblog import routes