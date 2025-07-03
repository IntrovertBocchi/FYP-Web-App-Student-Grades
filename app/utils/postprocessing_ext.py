# app/utils/postprocessing_ext.py
# Hides the backend logic for calculation / model integration
# Done for calculation purposes of manual fallback

import joblib
import warnings
from app.grade_formula import (
    calculate_inf_grade,
    calculate_cos_grade,
    calculate_adv_grade
)

# Load model once
_model = joblib.load('app/models/grade_predictor.pkcls')

try:
    import pickle
    with open('app/models/label_mapping.pkl', 'rb') as f:
        reverse_map = {v: k for k, v in pickle.load(f).items()}

except Exception as e:
    reverse_map = {}  # Fallback if label mapping isn't available
    print("Warning: Could not load label mapping:", e)

def map_score_to_grade(score):
    if score >= 80:
        return "HD"
    elif score >= 70:
        return "D"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "P"
    else:
        return "F"

def _run_prediction(subject, inputs):
    
    """
    This model was trained on 13 features, but is used program-specifically with subsets.
    Feature order is manually aligned.
    """
    source = "model"  # Assume model is used

    if subject == 'INF':
        model_input = [
            float(inputs['report_a']),
            float(inputs['report_b']),
            float(inputs['group_exercise']),
            float(inputs['cla_scores']),
            float(inputs['quiz_scores']),
        ]
        manual = calculate_inf_grade(inputs)

    elif subject == 'COS':
        model_input = [
            float(inputs['lab_exercises']),
            float(inputs['assignment1']),
            float(inputs['assignment2']),
            float(inputs['midterm']),
        ]
        manual = calculate_cos_grade(inputs)

    elif subject == 'ADV':
        model_input = [
            float(inputs['quiz_scores']),
            float(inputs['assignment1']),
            float(inputs['assignment2']),
            float(inputs['obow_test']),
        ]
        manual = calculate_adv_grade(inputs)
    else:
        raise ValueError("Unsupported subject")

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            prediction_output = _model.predict([model_input])
        
        # FIXED: Handle both iterable and scalar outputs
        if hasattr(prediction_output, '__iter__') and not isinstance(prediction_output, (str, bytes)):
            prediction = prediction_output[0]
        else:
            prediction = prediction_output

    except Exception:
        prediction = manual

    # Sanity check to fall back on manual if prediction is way off
    if abs(prediction - manual) > 5:
        prediction = manual

    rounded = round(prediction)
    grade_letter = map_score_to_grade(rounded)
    guidance = calculate_passing_guidance(subject,inputs,prediction)

    return {
        "predicted_score": round(prediction, 2),
        "predicted_grade": grade_letter,
        "source": source,
        "passing_guidance": guidance
    }


def calculate_passing_guidance(subject, inputs, score):
    PASS_MARK = 50.0

    if score >= PASS_MARK:
        return None  # No guidance needed

    needed = round(PASS_MARK - score, 2)

    if needed > 100:
        return "You cannot pass anymore — even scoring full marks won't help."
    else:
        return f"You need an overall of {needed}% more to pass the subject."
