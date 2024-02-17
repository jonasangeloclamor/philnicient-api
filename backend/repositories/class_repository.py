from backend.firebase_setup.firebase_config import db
from backend.data_components.models import Class
import uuid

def create_class(class_instance):
    doc_ref = db.collection('classes').document()
    class_instance.id = doc_ref.id
    class_instance.classcode = str(uuid.uuid4())[:8]
    doc_ref.set(class_instance.__dict__)
    return class_instance.id, class_instance.classcode

def get_class(class_id):
    doc_ref = db.collection('classes').document(class_id)
    doc = doc_ref.get()
    if doc.exists:
        return Class(**doc.to_dict())
    else:
        return None

def get_all_classes():
    classes = []
    docs = db.collection('classes').stream()
    for doc in docs:
        class_data = doc.to_dict()
        class_data['id'] = doc.id
        classes.append(Class(**class_data))
    return classes

def update_class(class_id, class_instance):
    doc_ref = db.collection('classes').document(class_id)
    doc_ref.update(class_instance)

def delete_class(class_id):
    db.collection('classes').document(class_id).delete()

def has_class(class_id):
    class_instance = get_class(class_id)
    return class_instance is not None
