from app import create_app
from app.models import db, GradeRange

app = create_app()

with app.app_context():
    # Clear table if needed
    db.session.query(GradeRange).delete()

    # Grade range definitions
    grades = [

        {"min_percentage": 80.0, "max_percentage": 100.0, "grade": "HD"},
        {"min_percentage": 70.0, "max_percentage": 79.99, "grade": "D"},
        {"min_percentage": 60.0, "max_percentage": 69.99, "grade": "C"},
        {"min_percentage": 50.0, "max_percentage": 59.99, "grade": "P"},
        {"min_percentage": 0.0, "max_percentage": 49.99, "grade": "F"},

    ]

    for g in grades:
        db.session.add(GradeRange(**g))

    db.session.commit()
    print("Grade ranges seeded successfully :D")
