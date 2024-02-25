from backend.firebase_setup.firebase_config import db
from backend.data_components.models import Result

def create_result(result):
    doc_ref = db.collection('results').document()
    result.id = doc_ref.id
    doc_ref.set(result.__dict__)
    return result.id

def get_result(result_id):
    doc_ref = db.collection('results').document(result_id)
    doc = doc_ref.get()
    if doc.exists:
        return Result(**doc.to_dict())
    else:
        return None

def get_all_results():
    results = []
    docs = db.collection('results').stream()
    for doc in docs:
        result_details = doc.to_dict()
        result_details['id'] = doc.id
        results.append(Result(**result_details))
    return results

def update_result(result_id, result):
    doc_ref = db.collection('results').document(result_id)
    doc_ref.update(result)

def get_result_by_student_id(student_id):
    query = db.collection('results').where('student_id', '==', student_id).limit(1)
    docs = query.stream()

    for doc in docs:
        return Result(**doc.to_dict())

    return None
