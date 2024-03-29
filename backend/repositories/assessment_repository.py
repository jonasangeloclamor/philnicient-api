from backend.firebase_setup.firebase_config import db
from backend.data_components.models import Assessment

def create_assessment(assessment):
    doc_ref = db.collection('assessments').document()
    assessment.id = doc_ref.id
    doc_ref.set(assessment.__dict__)
    return assessment.id

def get_assessment(assessment_id):
    doc_ref = db.collection('assessments').document(assessment_id)
    doc = doc_ref.get()
    if doc.exists:
        return Assessment(**doc.to_dict())
    else:
        return None

def get_all_assessments():
    assessments = []
    docs = db.collection('assessments').stream()
    for doc in docs:
        assessment_data = doc.to_dict()
        assessment_data['id'] = doc.id
        assessments.append(Assessment(**assessment_data))
    return assessments

def update_assessment(assessment_id, assessment):
    doc_ref = db.collection('assessments').document(assessment_id)
    doc_ref.update(assessment)
