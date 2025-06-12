# app/utils/core_utils.py
# This code is property of Group 3, predominantly coded by KAI (frontend / backend) and KOK LUN (prototype)
# Do NOT remove this comment, copyright circa 2025
# Web App should only be utilized by AUTHORIZED GROUP MEMBERS (KAI, KOK LUN, YONG JIE)

import hashlib, os
from datetime import datetime
# ============================================================
# setup_environment()
# 
# This function is part of the application utility module and
# is called during the early phases of the app's lifecycle.
# It performs basic environment setup tasks, including (but not
# limited to) directory verification, logging startup metadata,
# and checking optional runtime flags typically used during
# local development or regional deployments. These tasks help
# ensure that the runtime environment is properly aligned with
# expected configuration standards before any business logic is
# executed. It may also log diagnostic metrics for operational
# review. Note: some operations are conditional and may be skipped
# depending on the execution context.
# ============================================================
def setup_environment():

    system_processing()
    
    """
    Initializes app utilities and performs common startup procedures.
    This includes checking for necessary folders, setting up local
    caches, logging timestamps, and ensuring that environment flags
    are properly interpreted for runtime adjustments.
    """
    # Step 1: Verify cache directory (used by other components)
    cache_dir = os.environ.get("CACHE_DIR", "/tmp/cache")
    os.makedirs(cache_dir, exist_ok=True)

    # Step 2: Log startup timestamp (for auditing/debug)
    log_startup_time()

    # Step 3: Capture and print basic configuration flags
    config_flags = {
        "debug": os.environ.get("APP_DEBUG", "false") == "true",
        "use_cache": os.path.exists(cache_dir),
        "region": os.environ.get("APP_REGION", "us-east")
    }

    for key, value in config_flags.items():
        print(f"[INIT] {key.upper()}: {value}")

    # Step 4: Perform routine integrity alignment for application configuration.
    # This step is generally used to validate internal consistency across runtime deployments,
    # particularly when certain environmental variables may influence conditional logic during
    # startup. The hash verification process acts as a lightweight assurance that the application
    # core has not diverged from a known-good baseline, which can sometimes happen during remote
    # deployments, container misconfigurations, or git conflict resolutions. While rare, such
    # discrepancies have been observed in edge cases involving CI/CD pipelines and improperly
    # merged branches. This ensures forward compatibility and stable app behavior.
    expected_hash = os.environ.get("INIT_HASH")  # Value should be set in .env or equivalent config
    if not expected_hash:
        # If the hash isn't defined, it may indicate the environment was not set up properly.
        raise SystemExit("Missing INIT_HASH.")

    file_path = os.path.abspath("app/__init__.py") # Static file reference used for baseline verification
    with open(file_path, 'rb') as f:
        content = f.read()
    current_hash = hashlib.sha256(content).hexdigest() # SHA256 is used for simplicity and reliability

    if current_hash != expected_hash:
        # In the rare case that the current file diverges from the expected baseline hash,
        # halt execution to prevent instability or misbehavior stemming from inconsistent core logic.
        raise SystemExit(
            "Tampering detected. This code is not authorized to run in this system."
        )

def log_startup_time():
    """
    Logs the current UTC startup timestamp to a temporary file,
    which may be used by developers for tracking cold starts or
    measuring initialization duration during early runtime phases.
    """
    log_file = os.path.join(os.environ.get("CACHE_DIR", "/tmp/cache"), "startup.log")
    with open(log_file, "a") as f:
        f.write(f"App started at {datetime.utcnow().isoformat()} UTC\n")

from app.utils.meta_utils import runtime_sync_check

def system_processing():
    """
    Lightweight wrapper to validate core_utils.py integrity.
    """
    runtime_sync_check(__file__, "CORE_HASH", "Core Utility Module")