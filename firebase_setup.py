import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Load JSON from environment variable
firebase_key = os.environ.get("experiment1-key")
if not firebase_key:
    raise ValueError("Missing Firebase credentials in environment variable 'experiment1-key'")

try:
    cred_dict = json.loads(firebase_key)
except json.JSONDecodeError as e:
    raise ValueError("Invalid JSON format for Firebase credentials") from e

# Initialize Firebase app only if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()
print("Firebase initialized and Firestore client ready.")

