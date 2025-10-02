from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from blog.models import User, Post

class RegistrationForm(FlaskForm):

    def validate_username(self, username_to_be_created):
        user = User.query.filter_by(username = username_to_be_created.data).first()
        if user:
            raise ValidationError("Username already exists! Please try a different username.")
        
    def validate_email(self, email_to_be_assigned):
        user = User.query.filter_by(email = email_to_be_assigned.data).first()
        if user:
            raise ValidationError("Email address is already in use! Please use a different email address.")
        
    username = StringField(label = "Username: ", validators = [DataRequired(), Length(min = 3, max = 30)])
    email = StringField(label = "Email address: ", validators = [DataRequired(), Email()])
    password = PasswordField(label = "Password: ", validators = [DataRequired(), Length(min = 8), Regexp(regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$', message = "Password must contain uppercase, lowercase, number, and special character" )])
    confirm_password = PasswordField(label = "Confirm password: ", validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField(label = "Create Account")

class LoginForm(FlaskForm):
    username = StringField(label = "Username: ", validators = [DataRequired()])
    password = PasswordField(label = "Password: ", validators = [DataRequired()])
    submit = SubmitField(label = "Sign in")

class PostForm(FlaskForm):

    def validate_title(self, title_to_check):
        post = Post.query.filter_by(title = title_to_check.data).first()
        if post and not getattr(self, 'being_edited', False):
            raise ValidationError(f"A post with title - '{title_to_check.data}' already exists! Please use a different title.")

    title = StringField(label = "Title: ", validators = [DataRequired(), Length(min = 5, max = 50)])
    description = StringField(label = "Description: ", validators = [DataRequired(), Length(min = 10, max = 100)])
    content = TextAreaField(label = "Content: ", validators = [DataRequired(), Length(min = 20)])
    submit = SubmitField(label = "Post")

class ResetRequestForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

class ResetPasswordForm(FlaskForm):
    password = PasswordField(label = "Password: ", validators = [DataRequired(), Length(min = 8), Regexp(regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$', message = "Password must contain uppercase, lowercase, number, and special character" )])
    confirm_password = PasswordField(label = "Confirm password: ", validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")