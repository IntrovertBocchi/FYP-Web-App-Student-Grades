from flask import Flask, render_template, request, jsonify
from app.models import db
from app.predictor import predict_and_validate

def create_app():
    app = Flask(__name__)

    #Load config from config.py
    app.config.from_object('config.Config')

    #Initialize the database
    db.init_app(app)

    #Web page route
    @app.route('/')
    def index():
        return render_template('index.html') #renders templates/index.html

    #API for grade prediction
    @app.route('/api/predict', methods=['POST'])
    def predict():
        data = request.json
        subject = data.get('subject')
        inputs = data.get('inputs')

        if not subject or not inputs:
            return jsonify({'error': 'Missing subject or inputs'}), 400

        try:
            score = predict_and_validate(subject, inputs)
            return jsonify({'score': score})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    #Create database tables if needed
    with app.app_context():
        db.create_all()

    return app