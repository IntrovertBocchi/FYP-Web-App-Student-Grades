# seed_grades.py

# Import the app factory function and the GradeRange model
from app import create_app
from app.models import db, GradeRange

# Create an app instance
app = create_app()

# Create an application context so we can interact with the database
with app.app_context():

     # Optional: Clear the existing grade ranges (if reseeding)
    db.session.query(GradeRange).delete()

    # Define letter grades and their corresponding percentage ranges
    grades = [

        {"min_percentage": 80.0, "max_percentage": 100.0, "grade": "HD"},
        {"min_percentage": 70.0, "max_percentage": 79.99, "grade": "D"},
        {"min_percentage": 60.0, "max_percentage": 69.99, "grade": "C"},
        {"min_percentage": 50.0, "max_percentage": 59.99, "grade": "P"},
        {"min_percentage": 0.0, "max_percentage": 49.99, "grade": "F"},

    ]

    # Insert each grade range into the database
    for g in grades:
        db.session.add(GradeRange(**g)) # Unpack dictionary into model constructor

     # Commit the changes to persist the grade ranges
    db.session.commit()
    print("Grade ranges seeded successfully.")
