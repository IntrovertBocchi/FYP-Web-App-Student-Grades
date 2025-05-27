from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from app.models import db, User
from app.utils.core_utils import setup_environment
from app.predictor import predict_and_validate
import os
import json

from dotenv import load_dotenv #load .env support
load_dotenv() #Load variables from .env
setup_environment() #Sets up necessary environment for web application to run

MASTER_KEY =os.environ.get("MASTER_KEY")

def create_app():
    app = Flask(__name__)

    #Load config from config.py
    app.config.from_object('config.Config')

    #Initialize the database
    db.init_app(app)

    #Web page route
    @app.route('/')
    def index():
        if 'username' not in session:
            return redirect(url_for('login'))
        return render_template('index.html') #renders templates/index.html

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            master = request.form['master']

            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password) and master == MASTER_KEY:
                session['username'] = username
                return redirect(url_for('index'))
            else:
                return "Invalid credentials or master password", 403

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect(url_for('login'))
    

    #API for grade prediction
    @app.route('/api/predict', methods=['POST'])
    def predict():
        
        # Check if user is authenticated via session
        if 'username' not in session:
            return jsonify({'error': 'Unauthorized access'}), 403
    
        data = request.get_json()
        subject = data.get('subject')
        inputs = data.get('inputs')

        # 🛡️ Validate inputs before proceeding
        if not isinstance(inputs, dict):
            return jsonify({'error': 'Invalid input format: inputs must be a dictionary'}), 400

        try:
            result = predict_and_validate(subject, inputs)
            return jsonify(result)
        
        except Exception as e:
            print(f"Error during prediction: {e}")  # Helpful for server logs
            return jsonify({"error": str(e)}), 400

    
    #Accuracy score
    @app.route('/api/accuracy', methods=['GET'])
    def accuracy():

        try:
            with open('app/models/accuracy_score.txt') as f:
                acc = float(f.read())

            with open('app/models/accuracy_report.json') as f:
                full_report = json.load(f)

            # Mapping of numeric labels to letter grades
            label_map = {
                "0": "F",
                "1": "P",
                "2": "C",
                "3": "D",
                "4": "HD"
            }

            # Transform the full_report keys to human-readable grades
            details = {
                label_map[k]: {
                    "precision": round(float(v["precision"]), 2),
                    "recall": round(float(v["recall"]), 2)
                }
                for k, v in full_report.items() if k in label_map
            }

            return jsonify({
                "accuracy": round(acc, 3),
                "details": details
            })
        
        except Exception as e:
            print("ERROR in /api/accuracy:", str(e))  # Log to console
            return jsonify({"error": str(e)}), 500


    #Create database tables if needed
    with app.app_context():
        db.create_all()

    return app