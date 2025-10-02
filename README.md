# Flask Blog App

A modern, responsive blogging platform built with **Flask**, **SQLAlchemy**, and **Bootstrap 5**. Supports user authentication, email confirmation, password reset, and full CRUD operations for posts.

---

## Live Demo 
**_https://blog-app-five-eta.vercel.app/_**

---

## Features

- User registration, login, and logout
- Email confirmation for new accounts
- Password reset via email
- Create, edit, and delete posts
- Pagination for posts
- Responsive design with **Bootstrap 5**
- Flash messages for user feedback
- Secure password hashing with **Bcrypt**

---

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-Mail
- **Frontend:** HTML, Bootstrap 5, Jinja2
- **Database:** PostgreSQL (recommended for production), SQLite (for local testing)
- **Email Service:** Gmail SMTP or SendGrid API

---

## Installation

```bash
git clone https://github.com/nikgrinding/blog-app.git
cd blog-app
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file with:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://username:password@host:port/dbname
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**Notes:**
- For Gmail, enable [App Passwords](https://support.google.com/accounts/answer/185833?hl=en) if 2FA is on.
- For SendGrid, set `MAIL_USERNAME=apikey` and `MAIL_PASSWORD=your_sendgrid_api_key`.

---

## Running Locally

```bash
# Set Flask app
# Windows
set FLASK_APP=wsgi.py
# macOS/Linux
export FLASK_APP=wsgi.py

# Initialize database
flask shell
>>> from blog import db
>>> db.create_all()
>>> exit()

# Run server
flask run
```

Visit `http://127.0.0.1:5000` in your browser.

---

## Folder Structure

```
blog-app/
│
├─ blog/
│  ├─ __init__.py
│  ├─ routes.py
│  ├─ models.py
│  ├─ forms.py
│  ├─ utils.py
│  └─ templates/
│     ├─ base.html
│     ├─ home.html
│     ├─ login.html
│     ├─ register.html
│     ├─ posts.html
│     ├─ post_page.html
│     ├─ create_post.html
│     ├─ reset_request.html
│     ├─ reset_form.html
│     └─ email/
│        ├─ confirm.html
│        └─ reset.html
│
├─ venv/
├─ .env.example
├─ requirements.txt
└─ wsgi.py
```