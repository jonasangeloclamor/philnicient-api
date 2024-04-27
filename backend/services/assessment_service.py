from backend.repositories.assessment_repository import create_assessment, get_assessment, get_all_assessments, update_assessment, get_assessment_id_by_student_id, has_assessment, has_assessment_id, delete_assessment, is_assessment_for_student, get_all_assessments_by_class_id
from backend.repositories.student_repository import has_student_id
from backend.repositories.question_repository import delete_questions_by_assessment_id
from backend.repositories.user_repository import is_student
from backend.data_components.dtos import AssessmentCreationDto, AssessmentUpdationDto
from backend.data_components.mappings import map_assessment_creation_dto_to_model
from backend.utils.string_util import StringUtil

def create_assessment_service(assessment_data: AssessmentCreationDto):
    if not has_student_id(assessment_data.student_id):
        raise ValueError("Specified student_id is not currently available.")
    
    if has_assessment(assessment_data.student_id):
        raise ValueError("Student already has an assessment.")
    
    assessment_data.is_submitted = False
    
    assessment = map_assessment_creation_dto_to_model(assessment_data)
    assessment_id = create_assessment(assessment)
    assessment.id = assessment_id
    return assessment

def get_assessment_service(assessment_id):
    return get_assessment(assessment_id)

def get_all_assessments_service():
    return get_all_assessments()

def update_assessment_service(assessment_id, assessment_data: AssessmentUpdationDto):
    if not has_student_id(assessment_data.student_id):
        raise ValueError("Specified student_id is not currently available.") 
    existing_assessment = get_assessment(assessment_id)
    for key, value in assessment_data.__dict__.items():
        setattr(existing_assessment, key, value)
    existing_assessment.datetimeupdated = StringUtil.current_ph_time()
    update_assessment(assessment_id, existing_assessment.__dict__)

def get_assessment_id_by_student_id_service(student_id):
    return get_assessment_id_by_student_id(student_id)

def delete_assessment_service(assessment_id):
    if has_assessment_id(assessment_id):
        delete_questions_by_assessment_id(assessment_id)
    delete_assessment(assessment_id)

def is_assessment_for_student_service(assessment_id, user_id):
    if not is_student(user_id):
        raise ValueError("Specified user_id does not correspond to a student.")
    return is_assessment_for_student(assessment_id, user_id)

def get_all_assessments_by_class_id_service(class_id):
    return get_all_assessments_by_class_id(class_id)
