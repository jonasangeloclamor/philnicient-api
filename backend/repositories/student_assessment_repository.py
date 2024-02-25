from backend.firebase_setup.firebase_config import db
from backend.data_components.models import StudentAssessment

def create_student_assessment(student_assessment):
    doc_ref = db.collection('student_assessments').document()
    student_assessment.id = doc_ref.id
    doc_ref.set(student_assessment.__dict__)
    return student_assessment.id

def get_student_assessment(student_assessment_id):
    doc_ref = db.collection('student_assessments').document(student_assessment_id)
    doc = doc_ref.get()
    if doc.exists:
        return StudentAssessment(**doc.to_dict())
    else:
        return None

def get_all_student_assessments():
    student_assessments = []
    docs = db.collection('student_assessments').stream()
    for doc in docs:
        student_assessment_data = doc.to_dict()
        student_assessment_data['id'] = doc.id
        student_assessments.append(StudentAssessment(**student_assessment_data))
    return student_assessments

def update_student_assessment(student_assessment_id, student_assessment):
    doc_ref = db.collection('student_assessments').document(student_assessment_id)
    doc_ref.update(student_assessment)

def has_student_assessment_id(student_assessment_id):
    student_assessment = get_student_assessment(student_assessment_id)
    return student_assessment is not None
