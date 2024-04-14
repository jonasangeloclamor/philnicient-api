from backend.firebase_setup.firebase_config import db
from backend.data_components.models import Student

def create_student(student):
    doc_ref = db.collection('students').document()
    student.id = doc_ref.id
    doc_ref.set(student.__dict__)
    return student.id

def get_student(student_id):
    doc_ref = db.collection('students').document(student_id)
    doc = doc_ref.get()
    if doc.exists:
        return Student(**doc.to_dict())
    else:
        return None

def get_all_students():
    students = []
    docs = db.collection('students').stream()
    for doc in docs:
        student_data = doc.to_dict()
        student_data['id'] = doc.id
        students.append(Student(**student_data))
    return students

def delete_student(student_id):
    db.collection('students').document(student_id).delete()

def has_student_id(student_id):
    student = get_student(student_id)
    return student is not None

def get_students_by_class_id(class_id):
    students = []
    docs = db.collection('students').where('class_id', '==', class_id).stream()
    for doc in docs:
        student_data = doc.to_dict()
        student_data['id'] = doc.id
        students.append(Student(**student_data))
    return students

def is_student_in_class(student_id, class_id):
    student = get_student(student_id)
    return student and student.class_id == class_id
