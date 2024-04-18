from backend.repositories.user_repository import create_user, get_user, get_all_users, get_user_by_username, get_user_by_email, get_user_by_username_or_email, update_user_password, is_student, delete_user, is_teacher
from backend.repositories.class_repository import get_all_classes_by_teacher_id
from backend.services.class_service import delete_class_service
from backend.repositories.student_repository import get_students_by_student_id, delete_student
from backend.repositories.assessment_repository import get_assessment_id_by_student_id, delete_assessment
from backend.repositories.question_repository import delete_questions_by_assessment_id
from backend.repositories.assessment_result_repository import get_assessment_result_by_student_id, delete_assessment_result
from backend.data_components.dtos import UserCreationDto, UserLoginDto
from backend.data_components.mappings import map_user_creation_dto_to_model
import bcrypt
import re

def create_user_service(user_data: UserCreationDto):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user_data.email):
        raise ValueError("Invalid email format")

    user = map_user_creation_dto_to_model(user_data)
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    user_id = create_user(user)
    user.id = user_id
    return user

def get_user_service(user_id):
    return get_user(user_id)

def get_all_users_service():
    return get_all_users()

def get_user_by_username_service(username):
    return get_user_by_username(username)

def get_user_by_username_or_email_service(username_or_email):
    return get_user_by_username_or_email(username_or_email)

def get_user_by_email_service(email):
    return get_user_by_email(email)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def login_user(user_login_data: UserLoginDto):
    user = get_user_by_username_or_email(user_login_data.username_or_email)
    if user:
        if bcrypt.checkpw(user_login_data.password.encode('utf-8'), user.password.encode('utf-8')):
            return user
    return None

def update_user_password_service(email, new_password):
    user = get_user_by_email(email)
    if user:
        hashed_password = hash_password(new_password)
        user.password = hashed_password
        update_user_password(user.id, hashed_password)
    else:
        return None
    
def check_if_user_is_student_service(user_id):
    return is_student(user_id)

def delete_teacher_and_related_data_service(user_id):
    if not is_teacher(user_id):
        raise ValueError("Specified user ID does not correspond to a teacher.")

    classes = get_all_classes_by_teacher_id(user_id)   
    for class_ in classes:
        delete_class_service(class_.id)

    delete_user(user_id)

def delete_student_and_related_data_service(user_id):
    user = get_user(user_id)
    if user and is_student(user_id):
        students = get_students_by_student_id(user_id)
        for student in students:
            student_id = student.id
            delete_student(student_id)
            assessment_id = get_assessment_id_by_student_id(student_id)
            if assessment_id:
                delete_questions_by_assessment_id(assessment_id)
                delete_assessment(assessment_id)
                assessment_result = get_assessment_result_by_student_id(student_id)
                if assessment_result:
                    delete_assessment_result(assessment_result.id)
    
    delete_user(user_id)
