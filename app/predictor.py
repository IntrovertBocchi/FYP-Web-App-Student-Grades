# app/predictor.py 
import joblib
from app.grade_formula import (

    calculate_inf_grade,
    calculate_cos_grade,
    calculate_adv_grade

)

#load trained model once when app starts
model = joblib.load('app/models/predictor.pkcls')

def ensure_list(value):
    if isinstance(value, list):
        return value
    return [value]

def predict_and_validate(subject, inputs):

    """
    Predicts using .pkcls model and compares with manual calculation.
    If difference is too large, fallback to manual calculation.

    Parameters:
    - subject: 'INF', 'COS' or 'ADV'
    - inputs: a dict of required inputs, structure depends on subject

    Returns:
    - Final predicted or calculated grade (float)
    """

    # Converts input to model feature vector (i.e flatted nested lists)
    model_input = []

    if subject == 'INF':

        model_input = [
            
            inputs['report_a'],
            inputs['report_b'],
            inputs['group_exercise'],
            *ensure_list(inputs['cla_scores']),
            *ensure_list(inputs['quiz_scores']),

        ]

        manual = calculate_inf_grade(inputs)

    elif subject == 'COS':

        model_input = [

            *ensure_list(inputs['lab_exercises']),
            inputs['assignment1'],
            inputs['assignment2'],
            inputs['midterm'],

        ]

        manual = calculate_cos_grade(inputs)

    elif subject == 'ADV':

        model_input = [

            *ensure_list(inputs['quiz_scores']),
            inputs['assignment1'],
            inputs['assignment2'],
            inputs['obow_test'],
        ]

        manual = calculate_adv_grade(inputs)

    else:
        raise ValueError("Unsupported subject")
    
    prediction = model.predict([model_input])[0]

    if abs(prediction - manual) > 5:
        return manual
    return round(prediction, 2)