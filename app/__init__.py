# This code is property of Group 3, predominantly coded by KAI (frontend / backend) and KOK LUN (prototype)
# Do NOT remove this comment, copyright circa 2025

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from app.models import db, User
from app.utils.core_utils import setup_environment
from app.predictor import predict_and_validate
import os
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
setup_environment()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    # ✅ Load config from config.py (includes SECRET_KEY and DB settings)
    app.config.from_object('config.Config')

    # ✅ Session security improvements
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,       # Prevents access via JavaScript
        SESSION_COOKIE_SECURE=True,         # Ensures cookies are sent over HTTPS (enable only with HTTPS)
        SESSION_COOKIE_SAMESITE='Lax'       # Helps mitigate CSRF
    )

    # Initialize the database
    db.init_app(app)

    # Home route
    @app.route('/')
    def index():
        if 'username' not in session:
            return redirect(url_for('login'))
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            master = request.form['master']

            # ✅ Brute-force mitigation
            if 'login_attempts' not in session:
                session['login_attempts'] = 0

            if session['login_attempts'] >= 5:
                return "Too many failed login attempts. Try again later.", 429

            user = User.query.filter_by(username=username).first()
            master_key = os.environ.get("MASTER_KEY")

            if user and user.check_password(password) and master == master_key:
                session['username'] = username
                session.pop('login_attempts', None)  # ✅ Reset on success
                return redirect(url_for('index'))
            else:
                session['login_attempts'] += 1
                return "Invalid credentials or master password", 403

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect(url_for('login'))

    @app.route('/api/predict', methods=['POST'])
    def predict():
        if 'username' not in session:
            return jsonify({'error': 'Unauthorized access'}), 403

        data = request.get_json()
        subject = data.get('subject')
        inputs = data.get('inputs')

        # ✅ Validate input format
        if not isinstance(inputs, dict):
            return jsonify({'error': 'Invalid input format: inputs must be a dictionary'}), 400

        try:
            result = predict_and_validate(subject, inputs)
            return jsonify(result)
        except Exception as e:
            logger.error(f"Prediction error: {e}")  # ✅ Log internally
            return jsonify({"error": "An unexpected error occurred during prediction."}), 400

    @app.route('/api/accuracy', methods=['GET'])
    def accuracy():
        try:
            with open('app/models/accuracy_score.txt', encoding='utf-8') as f:
                acc = float(f.read())

            with open('app/models/accuracy_report.json', encoding='utf-8') as f:
                full_report = json.load(f)

            # Use grade labels directly
            grade_labels = ["F", "P", "C", "D", "HD"]

            details = {
                k: {
                    "precision": round(float(v["precision"]), 2),
                    "recall": round(float(v["recall"]), 2)
                }
                for k, v in full_report.items() if k in grade_labels
            }

            return jsonify({
                "accuracy": round(acc, 3),
                "details": details
            })

        except Exception as e:
            logger.error(f"Accuracy endpoint error: {e}")  # ✅ Avoid exposing internals
            return jsonify({"error": "Could not retrieve accuracy data."}), 500

    @app.route('/api/confusion_matrix')
    def get_confusion_matrix():
        try:
            with open("app/models/confusion_matrix.json", encoding='utf-8') as f:
                matrix_data = json.load(f)
            return jsonify(matrix_data)
        except Exception as e:
            logger.error(f"Confusion matrix load error: {e}")
            return jsonify({"error": "Failed to load confusion matrix."}), 500

    # ✅ Ensure DB tables are created
    with app.app_context():
        db.create_all()

    return app
