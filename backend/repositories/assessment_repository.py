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

def has_assessment_id(assessment_id):
    assessment = get_assessment(assessment_id)
    return assessment is not None

def get_assessment_id_by_student_id(student_id):
    query = db.collection('assessments').where('student_id', '==', student_id).limit(1)
    result = query.stream()
    for doc in result:
        return doc.id
    return None

def has_assessment(student_id):
    query = db.collection('assessments').where('student_id', '==', student_id).limit(1)
    result = query.stream()
    return len(list(result)) > 0

def delete_assessment(assessment_id):
    doc_ref = db.collection('assessments').document(assessment_id)
    doc_ref.delete()

def is_assessment_for_student(assessment_id, user_id):
    user_doc = db.collection('users').document(user_id).get()
    if user_doc.exists:
        user = user_doc.to_dict()
        if user['role'] != 'Student':
            return False
    else:
        return False
    
    assessment_doc = db.collection('assessments').document(assessment_id).get()
    if assessment_doc.exists:
        assessment = assessment_doc.to_dict()
        student_docs = db.collection('students').where('student_id', '==', user_id).stream()
        for doc in student_docs:
            student = doc.to_dict()
            if assessment['student_id'] == student['id']:
                return True
    return False
