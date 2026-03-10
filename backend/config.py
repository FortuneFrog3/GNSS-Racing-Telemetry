import os
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, db

load_dotenv()


def initialize_firebase():
    if not firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CRED_PATH")
        db_url = os.getenv("FIREBASE_DB_URL")

        if not cred_path:
            raise ValueError("FIREBASE_CRED_PATH environment variable not set.")

        if not db_url:
            raise ValueError("FIREBASE_DB_URL environment variable not set.")

        try:
            cred = credentials.Certificate(cred_path)
        except Exception as e:
            raise ValueError(f"Error loading Firebase credentials: {e}")

        firebase_admin.initialize_app(cred, {
            "databaseURL": db_url
        })


def get_db_reference(path="/"):
    return db.reference(path)                    
