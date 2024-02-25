from backend.repositories.result_repository import create_result, get_result, get_all_results, update_result, get_result_by_student_id
from backend.repositories.student_repository import has_student_id
from backend.data_components.dtos import ResultCreationDto, ResultUpdationDto
from backend.data_components.mappings import map_result_creation_dto_to_model
from backend.utils.string_util import StringUtil

def create_result_service(result_details: ResultCreationDto):
    if not has_student_id(result_details.student_id):
        raise ValueError("Specified student_id is not currently available.") 
    result = map_result_creation_dto_to_model(result_details)
    result_id = create_result(result)
    result.id = result_id
    return result

def get_result_service(result_id):
    return get_result(result_id)

def get_all_results_service():
    return get_all_results()

def update_result_service(result_id, result_details: ResultUpdationDto):
    if not has_student_id(result_details.student_id):
        raise ValueError("Specified student_id is not currently available.") 
    existing_result = get_result(result_id)
    for key, value in result_details.__dict__.items():
        setattr(existing_result, key, value)
    existing_result.datetimeupdated = StringUtil.get_current_datetime()
    update_result(result_id, existing_result.__dict__)

def get_result_by_student_id_service(student_id):
    return get_result_by_student_id(student_id)
