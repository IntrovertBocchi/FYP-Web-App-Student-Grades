# app/grade_formula.py

def calculate_inf_grade(data):

    """
    Manually calculates the total grade for INF subjects.

    Expected structure of 'data' dict:
    - report_a: float (out of 25)
    - report_b: float (out of 20)
    - group_exercise: float (out of 5)
    - cla_scores: float (out of 10, scaled to 30%)
    - quiz_scores: float (out of 15, scaled to 20%)

    Returns:
        float: Final grade percentage (rounded to 2 decimals)
    """

    total = (
        (data['report_a'] / 25) * 25 +
        (data['report_b'] / 20) * 20 +
        (data['group_exercise'] / 5) * 5 +
        (data['cla_scores'] / 10) * 30 +
        (data['quiz_scores'] / 15) * 20
    )
    return round(total, 2)

def calculate_cos_grade(data):

    """
    Manually calculates the total grade for COS subjects.

    Expected structure of 'data' dict:
    - lab_exercises: float (out of 10, scaled to 10%)
    - assignment1: float (out of 100)
    - assignment2: float (out of 100)
    - midterm: float (out of 35)

    Returns:
        float: Final grade percentage (rounded to 2 decimals)
    """

    total = (
        (data['lab_exercises'] / 10) * 10 +      # Single float, contributes 10%
        (data['assignment1'] / 100) * 30 +       # Contributes 30%
        (data['assignment2'] / 100) * 40 +       # Contributes 40%
        (data['midterm'] / 35) * 20              # Contributes 20%
    )

    return round(total, 2)
        

def calculate_adv_grade(data):

    """
    Manually calculates the total grade for ADV subjects.

    Expected structure of 'data' dict:
    - quiz_scores: float (out of 20, scaled to 20%)
    - assignment1: float (out of 10)
    - assignment2: float (out of 40)
    - obow_test: float (out of 30)

    Returns:
        float: Final grade percentage (rounded to 2 decimals)
    """

    total = (
        (data['quiz_scores'] / 20) * 20 +        # Single float, contributes 20%
        (data['assignment1'] / 10) * 10 +        # Contributes 10%
        (data['assignment2'] / 40) * 40 +        # Contributes 40%
        (data['obow_test'] / 30) * 30            # Contributes 30%
    )
    return round(total, 2)

