import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("backend/firebase_setup/key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
