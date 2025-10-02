from blog import app, db, mail
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from blog.forms import RegistrationForm, LoginForm, PostForm, ResetRequestForm, ResetPasswordForm
from blog.models import User, Post
from flask_mail import Message
from blog.utils import generate_token, confirm_token

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/register", methods = ["GET", "POST"])
def register_page():    
    form = RegistrationForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data, email = form.email.data, password = form.password.data)
        user_to_create.confirmed = False
        db.session.add(user_to_create)
        db.session.commit()
        token = generate_token(user_to_create.email, salt = "email-confirm")
        confirm_url = url_for("confirm_email", token = token, _external = True)
        html = render_template("email/confirm.html", confirm_url = confirm_url, user = user_to_create)
        msg = Message("Confirm your email for Blog App", recipients = [user_to_create.email], html = html)
        mail.send(msg)
        flash("Account created! Please check your email to confirm before logging in.", category = "info")
        return redirect(url_for("login_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg[0], category = "danger")
    return render_template("register.html", form = form)

@app.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token, salt = "email-confirm")
    if not email:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for("login_page"))
    user = User.query.filter_by(email = email).first_or_404()
    if user.confirmed:
        flash("Account already confirmed. Please log in.", category = "success")
    else:
        user.confirmed = True
        db.session.commit()
        flash("You have confirmed your account. Thanks!", category = "success")
    return redirect(url_for("login_page"))

@app.route("/reset_password", methods = ["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("posts_page"))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            token = generate_token(user.email, salt = "password-reset")
            reset_url = url_for("reset_token", token = token, _external = True)
            html = render_template("email/reset.html", reset_url = reset_url, user = user)
            msg = Message("Password reset for Blog App", recipients = [user.email], html = html)
            mail.send(msg)
        flash("If an account with that email exists, a reset link has been sent.", category = "info")
        return redirect(url_for("login_page"))
    return render_template("reset_request.html", form=form)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    email = confirm_token(token, salt = "password-reset", expiration = 3600)
    if not email:
        flash("That reset link is invalid or expired.", category = "danger")
        return redirect(url_for("reset_request"))
    user = User.query.filter_by(email = email).first_or_404()
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash("Your password has been reset. You can now log in.", category = "success")
        return redirect(url_for("login_page"))
    return render_template("reset_form.html", form=form)

@app.route("/login", methods = ["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if attempted_user:
            if not attempted_user.check_password(form.password.data):
                flash("Incorrect password! Please try again", category = "danger")
            elif not attempted_user.confirmed:
                flash("Please confirm your email before logging in.", category = "danger")
            else:
                login_user(attempted_user)
                flash(f"Login successful! You are logged in as: {attempted_user}", category = "success")
                return redirect(url_for("posts_page"))
        else:
            flash("User doesn't exist", category = "danger")
    return render_template("login.html", form = form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been successfully logged out!", category = "info")
    return redirect(url_for("home_page"))

@app.route("/posts", methods = ["GET", "POST"])
@login_required
def posts_page():
    if request.method == "GET":
        page = request.args.get('page', 1, type = int)
        posts = Post.query.order_by(Post.date_created.desc()).paginate(page = page, per_page = 9)
        user_posts = Post.query.filter_by(author_id = current_user.id).order_by(Post.date_created.desc()).all()
        return render_template("posts.html", posts = posts, user_posts = user_posts)

@app.route("/posts/<int:post_id>")
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_page.html", post = post)

@app.route("/posts/new", methods = ["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, description = form.description.data, content = form.content.data, author_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully!", category = "success")
        return redirect(url_for("posts_page"))
    return render_template("create_post.html", form = form)

@app.route("/posts/<int:post_id>/edit", methods = ["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        flash("You are not allowed to edit this post.", category = "danger")
        return redirect(url_for("posts_page"))
    form = PostForm(obj = post)
    form.being_edited = True
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated successfully!", category = "success")
        return redirect(url_for("view_post", post_id = post.id))
    return render_template("create_post.html", form = form, edit = True)

@app.route("/posts/<int:post_id>/delete", methods = ["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        flash("You are not allowed to delete this post.", category = "danger")
        return redirect(url_for("posts_page"))
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", category = "success")
    return redirect(url_for("posts_page"))