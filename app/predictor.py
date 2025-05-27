# app/predictor.py
"""
This module handles grade normalization and input preparation
for downstream analytic components.
"""

from app.utils.postprocessing_ext import _run_prediction

def predict_and_validate(subject, inputs):
    """
    Wraps the internal _run_prediction from postprocessing_ext.

    Args:
        subject (str): The subject code (e.g., "INF", "COS", "ADV").
        inputs (dict): The dictionary of input values.

    Returns:
        dict: {
        "predicted_score": float,
        "predicted_grade": str
        }
    """
    return _run_prediction(subject, inputs)



def dummy_predict(inputs):
    """ Legacy fallback, not used in production """
    return sum(inputs.values()) / len(inputs)