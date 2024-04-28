from backend.repositories.student_repository import create_student, get_student, get_all_students, delete_student, get_students_by_class_id, is_student_in_class
from backend.repositories.class_repository import has_class, get_all_classes_by_teacher_id
from backend.repositories.user_repository import is_student
from backend.repositories.assessment_repository import get_assessment_id_by_student_id, has_assessment_id, delete_assessment
from backend.repositories.question_repository import delete_questions_by_assessment_id
from backend.repositories.assessment_result_repository import get_assessment_result_by_student_id, delete_assessment_result
from backend.data_components.dtos import StudentCreationDto
from backend.data_components.mappings import map_student_creation_dto_to_model

def create_student_service(student_data: StudentCreationDto):
    if not has_class(student_data.class_id):
        raise ValueError("Specified class_id is not currently available.")
    if not is_student(student_data.student_id):
        raise ValueError("Specified student_id does not belong to a role of a student.")   
    student = map_student_creation_dto_to_model(student_data)
    student_id = create_student(student)
    student.id = student_id
    return student

def get_student_service(student_id):
    return get_student(student_id)

def get_all_students_service():
    return get_all_students()

def delete_student_service(student_id):
    if not get_student(student_id):
        raise ValueError("Specified student_id does not exist.")
    
    assessment_id = get_assessment_id_by_student_id(student_id)
    if assessment_id and has_assessment_id(assessment_id):
        delete_questions_by_assessment_id(assessment_id)
        delete_assessment(assessment_id)
    
    assessment_result = get_assessment_result_by_student_id(student_id)
    if assessment_result:
        delete_assessment_result(assessment_result.id)

    delete_student(student_id)

def get_students_by_class_id_service(class_id):
    return get_students_by_class_id(class_id)

def is_student_in_class_service(user_id, class_id):
    if not is_student(user_id):
        raise ValueError("Specified user_id does not correspond to a student.")
    return is_student_in_class(user_id, class_id)

def is_student_in_teacher_class(student_id, teacher_id):
    classes_taught_by_teacher = get_all_classes_by_teacher_id(teacher_id)
    for class_ in classes_taught_by_teacher:
        students_in_class = get_students_by_class_id(class_.id)
        for student in students_in_class:
            if student.id == student_id:
                return True
    return False
