from blog import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    password_hash = db.Column(db.String(), nullable = False)
    posts = db.relationship("Post", backref = "author", lazy = True)
    confirmed = db.Column(db.Boolean, nullable = False, default = False)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")
    @password.setter
    def password(self, password_to_be_set):
        self.password_hash = bcrypt.generate_password_hash(password_to_be_set).decode("utf-8")
    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def __repr__(self):
        return f"{self.username}"

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(50), unique = True, nullable = False)
    description = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text(), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    author_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable = False)