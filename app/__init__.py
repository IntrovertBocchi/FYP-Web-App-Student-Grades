from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from app.models import db, User
from app.utils.core_utils import setup_environment
from app.predictor import predict_and_validate
import os

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
        
        data = request.json
        entered_key = data.get('master_key')

        if entered_key != MASTER_KEY:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        subject = data.get('subject')
        inputs = data.get('inputs')

        if not subject or not inputs:
            return jsonify({'error': 'Missing subject or inputs'}), 400

        try:
            score = predict_and_validate(subject, inputs)
            return jsonify({'score': score})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    
    #Accuracy score
    @app.route('/api/accuracy', methods=['GET'])
    def accuracy():

        return jsonify({
            "accuracy": 0.87,
            "details": {
                "HD": {"precision": 0.91, "recall": 0.84},
                "D":  {"precision": 0.83, "recall": 0.78},
                "C":  {"precision": 0.75, "recall": 0.74},
                "P":  {"precision": 0.62, "recall": 0.66},
                "F":  {"precision": 0.95, "recall": 0.90}
            }
        })


    #Create database tables if needed
    with app.app_context():
        db.create_all()

    return app