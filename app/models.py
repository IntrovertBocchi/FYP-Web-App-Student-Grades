from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class GradeRange(db.Model):

    __tablename__ = 'grade_ranges'

    id = db.Column(db.Integer, primary_key=True)
    min_percentage = db.Column(db.Float, nullable=False)
    max_percentage = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5), nullable=False)

    @staticmethod
    def get_grade_for_percentage(percent):
        return GradeRange.query.filter(

            GradeRange.min_percentage <= percent,
            GradeRange.max_percentage >= percent

        ).first()
