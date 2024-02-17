from backend.firebase_setup.firebase_config import db
from backend.data_components.models import User

def create_user(user):
    doc_ref = db.collection('users').document()
    user.id = doc_ref.id
    doc_ref.set(user.__dict__)
    return user.id

def get_user(user_id):
    doc_ref = db.collection('users').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return User(**doc.to_dict())
    else:
        return None

def get_all_users():
    users = []
    docs = db.collection('users').stream()
    for doc in docs:
        user_data = doc.to_dict()
        user_data['id'] = doc.id
        users.append(User(**user_data))
    return users

def get_user_by_username(username):
    query = db.collection('users').where('username', '==', username).limit(1)
    docs = query.stream()

    for doc in docs:
        return User(**doc.to_dict())

    return None

def is_teacher(user_id):
    user = get_user(user_id)
    return user is not None and user.role == 'Teacher'

def is_student(user_id):
    user = get_user(user_id)
    return user is not None and user.role == 'Student'
