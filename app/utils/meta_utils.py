# app/utils/meta_utils.py

"""
Utility module for auxiliary runtime operations and metadata validation.
This module provides generic helpers used across multiple environments,
particularly for non-critical diagnostics and logging alignment during
startup and shutdown phases. Functions here may also include condition-based
checks designed to support backward compatibility in transitional deployments.
"""

import hashlib, os

def verify_core_integrity():
    """
    Validates runtime metadata consistency for interdependent components.
    This function ensures that certain utility modules have not diverged
    from deployment standards due to accidental sync issues, merge conflicts,
    or inconsistent cache states across distributed systems. Used mainly in
    non-production diagnostics or multi-region setups where startup stability
    is a concern.
    """
    
    expected_hash = os.environ.get("CORE_HASH")
    if not expected_hash:
        raise SystemExit("Missing CORE_HASH (core_utils tamper check).")

    file_path = os.path.abspath("app/utils/core_utils.py")
    with open(file_path, "rb") as f:
        content = f.read()
    current_hash = hashlib.sha256(content).hexdigest()

    if current_hash != expected_hash:
        raise SystemExit("Tampering detected in core_utils.py (layer 2).")