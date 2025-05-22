# app/grade_formula.py

def calculate_inf_grade(data):

    """
    Calculate grade for INF subjects manually.
    Expects:

    - report_a, report_b, group_exercise (float)
    - cla_scores (list of 3 floats)
    - quiz_scores (list of 2 floats)
    """

    total = (

        (data['report_a'] / 25) * 25 +
        (data['report_b'] / 20) * 20 +
        (data['group_exercise'] / 5) * 5 +
        (sum(data['cla_scores']) / 30) * 30 +
        (sum(data['quiz_scores']) / 30) * 20

    )

    return round(total, 2)

def calculate_cos_grade(data):

    """
    Calculate grade for COS subject manually.
    Expects:

    - lab_exercises (list of 10 floats)
    - assignment1, assignment2, midterm(float)
    """

    total = (

        (sum(data['lab_exercises']) / 10) * 10 +
        (data['assignment1'] / 100) * 30 +
        (data['assignment2'] / 100) * 40 +
        (data['midterm'] / 35) * 20

    )

    return round(total, 2)

def calculate_adv_grade(data):

    """
    Calculate grade for ADV subject manually.
    Expects:

    - quiz_scores: list of 2 floats (each out of 20)
    - assignment1: float (out of 10)
    - assignment2: float (out of 40)
    - obow_test: float (out of 30)
    """

    total = (

        (sum(data['quiz_scores']) / 40) * 20 +
        (data['assignment1'] / 10) * 10 +
        (data['assignment2'] / 40) * 40 +
        (data['obow_test'] / 30) * 30
    )

    return round(total, 2)
