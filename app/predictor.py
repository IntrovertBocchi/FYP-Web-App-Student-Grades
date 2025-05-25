# app/predictor.py
"""
This module handles grade normalization and input preparation
for downstream analytic components.
"""

from app.utils.postprocessing_ext import _run_prediction as predict_and_validate

def dummy_predict(inputs):
    """ Legacy fallback, not used in production """
    return sum(inputs.values()) / len(inputs)