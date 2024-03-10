from backend.firebase_setup.firebase_config import db
from backend.data_components.models import AssessmentResult

def create_assessment_result(assessment_result):
    doc_ref = db.collection('assessment_results').document()
    assessment_result.id = doc_ref.id
    doc_ref.set(assessment_result.__dict__)
    return assessment_result.id

def get_assessment_result(assessment_result_id):
    doc_ref = db.collection('assessment_results').document(assessment_result_id)
    doc = doc_ref.get()
    if doc.exists:
        return AssessmentResult(**doc.to_dict())
    else:
        return None

def get_all_assessment_results():
    assessment_results = []
    docs = db.collection('assessment_results').stream()
    for doc in docs:
        assessment_result_details = doc.to_dict()
        assessment_result_details['id'] = doc.id
        assessment_results.append(AssessmentResult(**assessment_result_details))
    return assessment_results

def get_assessment_result_by_student_id(student_id):
    query = db.collection('assessment_results').where('student_id', '==', student_id).limit(1)
    docs = query.stream()

    for doc in docs:
        return AssessmentResult(**doc.to_dict())

    return None
