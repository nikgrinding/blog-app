from blog import app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

def generate_token(email, salt = "email-confirm"):
    return serializer.dumps(email, salt = salt)

def confirm_token(token, salt = "email-confirm", expiration = 3600):
    try:
        email = serializer.loads(token, salt = salt, max_age = expiration)
    except (SignatureExpired, BadTimeSignature):
        return None
    return email