from flask import Flask, request, render_template, jsonify, redirect, session
from flask_session import Session
import secrets
import os

app = Flask(__name__)

# Set a secret key for sessions
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Configure server-side sessions
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

# Correct inputs (store securely)
CORRECT_INPUTS = [
    "C'est juste une page #FFFFFF",
    "C'est juste une page #000000"
]

# Redirect URL (configure as needed)
REDIRECT_URL = "https://example.com"

@app.route('/', methods=['GET'])
def index():
    # Generate a unique session token to prevent replay attacks
    session['challenge_token'] = secrets.token_urlsafe(32)
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    # Get the input and session token
    user_input = request.form.get('input', '').strip()
    submitted_token = request.form.get('token')
    
    # Verify session token to prevent CSRF
    if not submitted_token or submitted_token != session.get('challenge_token'):
        return jsonify({
            'status': 'error',
            'message': 'Invalid session. Please refresh the page.'
        }), 400
    
    # Validate input
    if user_input in CORRECT_INPUTS:
        # Clear the challenge token after successful verification
        session.pop('challenge_token', None)
        return jsonify({
            'status': 'success',
            'redirect': REDIRECT_URL
        })
    
    return jsonify({
        'status': 'error',
        'message': 'Try again next time!'
    }), 400

if __name__ == '__main__':
    # Ensure a secure random secret key
    app.run(debug=False, ssl_context='adhoc')