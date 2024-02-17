from backend.repositories.student_repository import create_student, get_student, get_all_students, delete_student, get_students_by_class_id
from backend.repositories.class_repository import has_class
from backend.repositories.user_repository import is_student
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
    return delete_student(student_id)

def get_students_by_class_id_service(class_id):
    return get_students_by_class_id(class_id)
