from backend.repositories.assessment_result_repository import create_assessment_result, get_assessment_result, get_all_assessment_results, update_assessment_result, get_assessment_result_by_student_id, has_assessment_result_by_student_id
from backend.repositories.student_repository import has_student_id
from backend.data_components.dtos import AssessmentResultCreationDto, AssessmentResultUpdationDto
from backend.data_components.mappings import map_assessment_result_creation_dto_to_model
from backend.utils.string_util import StringUtil

def create_assessment_result_service(assessment_result_details: AssessmentResultCreationDto):
    if not has_student_id(assessment_result_details.student_id):
        raise ValueError("Specified student_id is not currently available.") 
    if has_assessment_result_by_student_id(assessment_result_details.student_id):
        raise ValueError("Student already has an assessment result.")
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
    existing_assessment_result = get_assessment_result(assessment_result_id)
    for key, value in assessment_result_details.__dict__.items():
        setattr(existing_assessment_result, key, value)
    existing_assessment_result.datetimeupdated = StringUtil.current_ph_time()
    update_assessment_result(assessment_result_id, existing_assessment_result.__dict__)

def get_assessment_result_by_student_id_service(student_id):
    return get_assessment_result_by_student_id(student_id)
