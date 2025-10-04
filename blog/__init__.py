import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
db_url = os.getenv("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config.update({
    "MAIL_SERVER": os.getenv("MAIL_SERVER"),
    "MAIL_PORT": int(os.getenv("MAIL_PORT")),
    "MAIL_USE_TLS": os.getenv("MAIL_USE_TLS") == "True",
    "MAIL_USERNAME": os.getenv("MAIL_USERNAME"),
    "MAIL_PASSWORD": os.getenv("MAIL_PASSWORD"),
    "MAIL_DEFAULT_SENDER": os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME"))
})

db = SQLAlchemy(app)

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

mail = Mail(app)

csrf = CSRFProtect(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from blog import routes, models