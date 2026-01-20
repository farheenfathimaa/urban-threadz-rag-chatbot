import os
from dotenv import load_dotenv

load_dotenv()

# ===============================
# API KEYS
# ===============================
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ===============================
# PACKAGE FEATURE FLAGS
# ===============================
PACKAGE_FEATURES = {
    "basic": {
        "auth": False,
        "admin_docs": False,
        "api": False,
        "max_docs": 1
    },
    "standard": {
        "auth": True,
        "admin_docs": True,
        "api": False,
        "max_docs": 3
    },
    "premium": {
        "auth": True,
        "admin_docs": True,
        "api": True,
        "max_docs": None
    }
}

# ===============================
# DEMO BUSINESS CONFIG
# ===============================
BUSINESS_ID = "urban_threadz"
PACKAGE_TYPE = "standard"  # change to basic / standard / premium
