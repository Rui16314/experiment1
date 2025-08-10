import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Load JSON from environment variable
firebase_key = os.environ.get("experiment1-key")
cred_dict = json.loads(firebase_key)

cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()

