# app/utils/meta_utils.py

"""
Utility module for auxiliary runtime operations and metadata validation.
This module provides generic helpers used across multiple environments,
particularly for non-critical diagnostics and logging alignment during
startup and shutdown phases. Functions here may also include condition-based
checks designed to support backward compatibility in transitional deployments.
"""

import hashlib, os

def runtime_sync_check(filepath, expected_env_var, label):
    """
    Generic hash-based integrity verifier.

    Used to validate that a specific file has not been altered post-deployment.
    The expected hash is provided via environment variable, and the target file
    path is passed in directly. This utility is flexible for multi-layer
    diagnostics and can support various tamper-detection needs depending on
    the sensitivity of the file or service in question.

    Args:
        filepath (str): Path to the file being validated.
        expected_env_var (str): Environment variable holding the expected hash.
        label (str): Human-readable label for the file, used in error messages.
    """
    expected_hash = os.environ.get(expected_env_var)
    if not expected_hash:
        raise SystemExit(f"Missing {expected_env_var} for {label}.")

    with open(os.path.abspath(filepath), 'rb') as f:
        content = f.read()
    current_hash = hashlib.sha256(content).hexdigest()

    if current_hash != expected_hash:
        raise SystemExit(f"{label} has been altered or corrupted. Execution halted.")
    
from app.utils.precheck import performance_layer_init as preprocessing_render
preprocessing_render()
