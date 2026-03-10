from firebase_admin import db
from backend.config import initialize_firebase

try:
    initialize_firebase()
except ValueError:
    # Credentials not available (e.g., in CI/CD or tests)
    pass



# return a database reference to the specified path
def get_ref(path: str = "/"):
    return db.reference(path)

def write_data(path: str, data: dict):
    ref = get_ref(path)
    ref.set(data)

def read_data(path: str):
    ref = get_ref(path)
    return ref.get()