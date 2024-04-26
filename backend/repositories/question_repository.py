from backend.firebase_setup.firebase_config import db
from backend.data_components.models import Question

def create_questions(questions):
    batch = db.batch()
    question_ids = []

    for question in questions:
        doc_ref = db.collection('questions').document()
        question.id = doc_ref.id
        batch.set(doc_ref, question.__dict__)
        question_ids.append(question.id)

    batch.commit()
    return question_ids

def get_question(question_id):
    doc_ref = db.collection('questions').document(question_id)
    doc = doc_ref.get()
    if doc.exists:
        return Question(**doc.to_dict())
    else:
        return None

def get_all_questions():
    questions = []
    docs = db.collection('questions').stream()
    for doc in docs:
        question_data = doc.to_dict()
        question_data['id'] = doc.id
        questions.append(Question(**question_data))
    return questions

def update_question(question_id, question):
    doc_ref = db.collection('questions').document(question_id)
    doc_ref.update(question)

def delete_question(question_id):
    doc_ref = db.collection('questions').document(question_id)
    doc_ref.delete()

def delete_questions_by_assessment_id(assessment_id):
    docs = db.collection('questions').where('assessment_id', '==', assessment_id).stream()
    for doc in docs:
        doc.reference.delete()
        