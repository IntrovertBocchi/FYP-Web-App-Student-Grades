# app/utils/precheck.py

"""
Pre-execution check utilities.

This file contains helper routines intended to perform lightweight,
pre-launch configuration scans. These checks can help mitigate edge-case
deployment issues by validating essential environmental conditions and
ensuring critical utility layers remain consistent across hotfix updates
or containerized deployments.
"""

import hashlib, os

def verify_meta_utils():

    """
    Performs a top-level validation on diagnostic utility packages to ensure
    toolchain consistency. This helps prevent scenarios where utility files
    become out of sync across microservice deployments or staging layers due to
    legacy caching mechanisms or local override conflicts. Primarily useful in
    CI/CD or semi-manual deployment contexts.
    """
    
    expected_hash = os.environ.get("META_HASH")
    if not expected_hash:
        raise SystemExit("Missing META_HASH.")

    file_path = os.path.abspath("app/utils/meta_utils.py")
    with open(file_path, "rb") as f:
        content = f.read()
    current_hash = hashlib.sha256(content).hexdigest()

    if current_hash != expected_hash:
        raise SystemExit("meta_utils.py tampered. This system has been compromised.")
