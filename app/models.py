from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
