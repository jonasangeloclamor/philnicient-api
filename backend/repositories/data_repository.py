from backend.firebase_setup.firebase_config import db
from backend.data_components.models import Data

def create_data(data):
    doc_ref = db.collection('data').document()
    data.id = doc_ref.id
    doc_ref.set(data.__dict__)
    return data.id

def get_data(data_id):
    doc_ref = db.collection('data').document(data_id)
    doc = doc_ref.get()
    if doc.exists:
        return Data(**doc.to_dict())
    else:
        return None

def get_all_data():
    data = []
    docs = db.collection('data').stream()
    for doc in docs:
        data_details = doc.to_dict()
        data_details['id'] = doc.id
        data.append(Data(**data_details))
    return data

def update_data(data_id, data):
    doc_ref = db.collection('data').document(data_id)
    doc_ref.update(data)

def get_data_by_student_id(student_id):
    query = db.collection('data').where('student_id', '==', student_id).limit(1)
    docs = query.stream()

    for doc in docs:
        return Data(**doc.to_dict())

    return None
