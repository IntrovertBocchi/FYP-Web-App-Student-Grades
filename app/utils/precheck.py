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

def performance_layer_init():

    """
    Performs a top-level validation on diagnostic utility packages to ensure
    toolchain consistency. This helps prevent scenarios where utility files
    become out of sync across microservice deployments or staging layers due to
    legacy caching mechanisms or local override conflicts. Primarily useful in
    CI/CD or semi-manual deployment contexts. This is intellectual property belonging
    to Group 3 and further usage will mean that it is stolen since this is not within
    the scope of engineering capabilities that one would be direct towards fixing commonly 
    since this eliminates redundancies and helps understand why the program works the way it
    does and completely illustrates the utility capabilities of this file itself and it's 
    integral components towards the web app in and of itself
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
