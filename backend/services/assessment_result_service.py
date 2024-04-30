from backend.repositories.assessment_result_repository import create_assessment_result, get_assessment_result, get_all_assessment_results, update_assessment_result, get_assessment_result_by_student_id, delete_assessment_result, has_assessment_result_by_student_id
from backend.repositories.student_repository import has_student_id, is_student_enrolled_in_class
from backend.repositories.class_repository import get_class_ids_by_teacher_id
from backend.data_components.dtos import AssessmentResultCreationDto, AssessmentResultUpdationDto
from backend.data_components.mappings import map_assessment_result_creation_dto_to_model
from backend.utils.string_util import StringUtil

def create_assessment_result_service(assessment_result_details: AssessmentResultCreationDto):
    if not has_student_id(assessment_result_details.student_id):
        raise ValueError("Specified student_id is not currently available.")
    
    if has_assessment_result_by_student_id(assessment_result_details.student_id):
        raise ValueError("Student already has an assessment result.")
    
    teacher_id = assessment_result_details.teacher_id
    class_ids = get_class_ids_by_teacher_id(teacher_id)
    if not class_ids:
        raise ValueError("Specified teacher_id is not associated with any class.")
    
    if not is_student_enrolled_in_class(assessment_result_details.student_id, class_ids):
        raise ValueError("Specified student_id is not enrolled in any class taught by the specified teacher.") 

    assessment_result = map_assessment_result_creation_dto_to_model(assessment_result_details)
    assessment_result_id = create_assessment_result(assessment_result)
    assessment_result.id = assessment_result_id
    return assessment_result

def get_assessment_result_service(assessment_result_id):
    return get_assessment_result(assessment_result_id)

def get_all_assessment_results_service():
    return get_all_assessment_results()

def update_assessment_result_service(assessment_result_id, assessment_result_details: AssessmentResultUpdationDto):
    if not has_student_id(assessment_result_details.student_id):
        raise ValueError("Specified student_id is not currently available.") 

    teacher_id = assessment_result_details.teacher_id
    class_ids = get_class_ids_by_teacher_id(teacher_id)
    if not class_ids:
        raise ValueError("Specified teacher_id is not associated with any class.")
    
    if not is_student_enrolled_in_class(assessment_result_details.student_id, class_ids):
        raise ValueError("Specified student_id is not enrolled in any class taught by the specified teacher.") 

    existing_assessment_result = get_assessment_result(assessment_result_id)
    
    if teacher_id != existing_assessment_result.teacher_id:
        raise ValueError("Unauthorized to modify assessment result.")

    for key, value in assessment_result_details.__dict__.items():
        setattr(existing_assessment_result, key, value)
    existing_assessment_result.datetimeupdated = StringUtil.current_ph_time()
    update_assessment_result(assessment_result_id, existing_assessment_result.__dict__)

def get_assessment_result_by_student_id_service(student_id):
    return get_assessment_result_by_student_id(student_id)

def delete_assessment_result_service(assessment_result_id):
    return delete_assessment_result(assessment_result_id)
