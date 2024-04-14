import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os

load_dotenv()

type = os.getenv('FIREBASE_TYPE')
project_id = os.getenv('FIREBASE_PROJECT_ID')
private_key_id = os.getenv('FIREBASE_PRIVATE_KEY_ID')
private_key = os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n')
client_email = os.getenv('FIREBASE_CLIENT_EMAIL')
client_id = os.getenv('FIREBASE_CLIENT_ID')
auth_uri = os.getenv('FIREBASE_AUTH_URI')
token_uri = os.getenv('FIREBASE_TOKEN_URI')
auth_provider_x509_cert_url = os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL')
client_x509_cert_url = os.getenv('FIREBASE_CLIENT_X509_CERT_URL')
universe_domain = os.getenv('FIREBASE_UNIVERSE_DOMAIN')

cred = credentials.Certificate({
    "type": type,
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": auth_uri,
    "token_uri": token_uri,
    "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
    "client_x509_cert_url": client_x509_cert_url,
    "universe_domain": universe_domain
})

firebase_admin.initialize_app(cred)
db = firestore.client()
