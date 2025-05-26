# app/grade_formula.py

def calculate_inf_grade(data):

    """
    Manually calculates the total grade for INF subjects.

    Expected structure of 'data' dict:
    - report_a: float (out of 25)
    - report_b: float (out of 20)
    - group_exercise: float (out of 5)
    - cla_scores: list of 3 floats (total out of 30)
    - quiz_scores: list of 2 floats (total out of 30, scaled down to 20)

    Returns:
        float: Final grade percentage (rounded to 2 decimals)
    """

    total = (

        (data['report_a'] / 25) * 25 +          # Report A contributes 25%
        (data['report_b'] / 20) * 20 +          # Report B contributes 20%
        (data['group_exercise'] / 5) * 5 +      # Group Exercise contributes 5%
        (sum(data['cla_scores']) / 30) * 30 +   # CLAs (3 parts) contribute 30%
        (sum(data['quiz_scores']) / 30) * 20    # Quizzes (2 parts) contribute 20%

    )

    return round(total, 2)

def calculate_cos_grade(data):

    """
    Manually calculates the total grade for COS subjects.

    Expected structure of 'data' dict:
    - lab_exercises: list of 10 floats (each out of 1, total out of 10)
    - assignment1: float (out of 100)
    - assignment2: float (out of 100)
    - midterm: float (out of 35)

    Returns:
        float: Final grade percentage (rounded to 2 decimals)
    """

    total = (

        (sum(data['lab_exercises']) / 10) * 10 +        # Lab exercises contribute 10%
        (data['assignment1'] / 100) * 30 +              # Assignment 1 contributes 30%
        (data['assignment2'] / 100) * 40 +              # Assignment 2 contributes 40%
        (data['midterm'] / 35) * 20                     # Midterm contributes 20%

    )

    return round(total, 2)

def calculate_adv_grade(data):

    """
    Manually calculates the total grade for ADV subjects.

    Expected structure of 'data' dict:
    - quiz_scores: list of 2 floats (each out of 20, total out of 40)
    - assignment1: float (out of 10)
    - assignment2: float (out of 40)
    - obow_test: float (out of 30)

    Returns:
        float: Final grade percentage (rounded to 2 decimals)
    """

    total = (

        (sum(data['quiz_scores']) / 40) * 20 +      # Quizzes contribute 20%
        (data['assignment1'] / 10) * 10 +           # Assignment 1 contributes 10%
        (data['assignment2'] / 40) * 40 +           # Assignment 2 contributes 40%
        (data['obow_test'] / 30) * 30               # OBoW test contributes 30%
    )

    return round(total, 2)
