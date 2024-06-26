from backend.firebase_setup.firebase_config import db
from backend.data_components.models import ModelResult

def create_multiple_model_results(model_results):
    batch = db.batch()
    model_result_ids = []

    for model_result in model_results:
        doc_ref = db.collection('model_results').document()
        model_result.id = doc_ref.id
        batch.set(doc_ref, model_result.__dict__)
        model_result_ids.append(model_result.id)

    batch.commit()
    return model_result_ids

def update_multiple_model_results(model_results):
    batch = db.batch()
    for model_result in model_results:
        model_result_id = model_result.get("id")
        if model_result_id:
            doc_ref = db.collection('model_results').document(model_result_id)
            batch.update(doc_ref, model_result)
    batch.commit()

def get_model_results_by_ids(model_result_ids):
    model_results = []
    batch = db.batch()

    for model_result_id in model_result_ids:
        doc_ref = db.collection('model_results').document(model_result_id)
        batch.get(doc_ref)

    results = batch.commit()
    for result in results:
        doc = result[1]
        if doc.exists:
            model_results.append(ModelResult(**doc.to_dict()))

    return model_results

def create_model_result(model_result):
    doc_ref = db.collection('model_results').document()
    model_result.id = doc_ref.id
    doc_ref.set(model_result.__dict__)
    return model_result.id

def get_model_result(model_result_id):
    doc_ref = db.collection('model_results').document(model_result_id)
    doc = doc_ref.get()
    if doc.exists:
        return ModelResult(**doc.to_dict())
    else:
        return None

def get_all_model_results():
    model_results = []
    docs = db.collection('model_results').stream()
    for doc in docs:
        model_result_details = doc.to_dict()
        model_result_details['id'] = doc.id
        model_results.append(ModelResult(**model_result_details))
    return model_results

def update_model_result(model_result_id, model_result):
    doc_ref = db.collection('model_results').document(model_result_id)
    doc_ref.update(model_result)

def get_model_result_by_student_id(student_id):
    query = db.collection('model_results').where('student_id', '==', student_id).limit(1)
    docs = query.stream()

    for doc in docs:
        return ModelResult(**doc.to_dict())

    return None

def delete_model_result(model_result_id):
    db.collection('model_results').document(model_result_id).delete()

def get_model_result_by_student_id_and_major_category(student_id, major_category):
    query = db.collection('model_results').where('student_id', '==', student_id).where('major_category', '==', major_category).limit(1)
    docs = query.stream()

    for doc in docs:
        return ModelResult(**doc.to_dict())

    return None

def get_number_of_model_results_for_student(student_id):
    query = db.collection('model_results').where('student_id', '==', student_id)
    return len(query.get())

def get_model_result_by_major_category(major_category):
    query = db.collection('model_results').where('major_category', '==', major_category).limit(1)
    docs = query.stream()

    for doc in docs:
        return ModelResult(**doc.to_dict())

    return None

def has_model_result_id(model_result_id):
    doc_ref = db.collection('model_results').document(model_result_id)
    doc = doc_ref.get()
    return doc.exists

def get_model_result_by_student_id_and_teacher_id(student_id, teacher_id):
    query = db.collection('model_results').where('student_id', '==', student_id).where('teacher_id', '==', teacher_id).limit(1)
    docs = query.stream()

    for doc in docs:
        return ModelResult(**doc.to_dict())

    return None
   