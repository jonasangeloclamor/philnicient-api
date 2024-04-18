from backend.firebase_setup.firebase_config import db
from backend.data_components.models import User
from backend.utils.string_util import StringUtil

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

def get_user_by_email(email):
    query = db.collection('users').where('email', '==', email).limit(1)
    docs = query.stream()

    for doc in docs:
        return User(**doc.to_dict())

    return None

def get_user_by_username(username):
    query = db.collection('users').where('username', '==', username).limit(1)
    docs = query.stream()

    for doc in docs:
        return User(**doc.to_dict())

    return None

def get_user_by_username_or_email(username_or_email):
    query = db.collection('users').where('username', '==', username_or_email).limit(1)
    docs = query.stream()

    for doc in docs:
        return User(**doc.to_dict())

    query = db.collection('users').where('email', '==', username_or_email).limit(1)
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

def update_user_password(user_id, new_password):
    user = get_user(user_id)
    if user:
        user.password = new_password
        user.datetimeupdated = StringUtil.current_ph_time()
        doc_ref = db.collection('users').document(user_id)
        doc_ref.update({'password': new_password, 'datetimeupdated': user.datetimeupdated})
    else:
        return None
    
def delete_user(user_id):
    db.collection('users').document(user_id).delete()
