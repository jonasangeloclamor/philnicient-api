from backend.repositories.assessment_result_repository import create_assessment_result, get_assessment_result, get_all_assessment_results, get_assessment_result_by_student_id
from backend.repositories.student_repository import has_student_id
from backend.data_components.dtos import AssessmentResultCreationDto
from backend.data_components.mappings import map_assessment_result_creation_dto_to_model

def create_assessment_result_service(assessment_result_details: AssessmentResultCreationDto):
    if not has_student_id(assessment_result_details.student_id):
        raise ValueError("Specified student_id is not currently available.") 
    assessment_result = map_assessment_result_creation_dto_to_model(assessment_result_details)
    assessment_result_id = create_assessment_result(assessment_result)
    assessment_result.id = assessment_result_id
    return assessment_result

def get_assessment_result_service(assessment_result_id):
    return get_assessment_result(assessment_result_id)

def get_all_assessment_results_service():
    return get_all_assessment_results()

def get_assessment_result_by_student_id_service(student_id):
    return get_assessment_result_by_student_id(student_id)
