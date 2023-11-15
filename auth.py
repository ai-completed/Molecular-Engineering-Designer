from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
from flask import request, jsonify

# TODO: Store this in a more secure place
SECRET_KEY = 'your_secret_key'

# Mock database for users
# TODO: Replace with real database integration
users_db = {
    'admin': generate_password_hash('admin_pass')
}

# Authentication decorator to verify user credentials
def authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({'message': 'Authentication required.'}), 401

        user = users_db.get(auth.username)
        if not user or not check_password_hash(user, auth.password):
            return jsonify({'message': 'Bad credentials'}), 401
        
        return f(*args, **kwargs)
    return decorated

# Authorization decorator to verify tokens
def authorize(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated