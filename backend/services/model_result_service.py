from backend.repositories.model_result_repository import create_model_result, get_model_result, get_all_model_results, update_model_result, get_model_result_by_student_id
from backend.repositories.student_repository import has_student_id
from backend.data_components.dtos import ModelResultCreationDto, ModelResultUpdationDto
from backend.data_components.mappings import map_model_result_creation_dto_to_model
from backend.utils.string_util import StringUtil

def create_model_result_service(model_result_details: ModelResultCreationDto):
    if not has_student_id(model_result_details.student_id):
        raise ValueError("Specified student_id is not currently available.") 
    model_result = map_model_result_creation_dto_to_model(model_result_details)
    model_result_id = create_model_result(model_result)
    model_result.id = model_result_id
    return model_result

def get_model_result_service(model_result_id):
    return get_model_result(model_result_id)

def get_all_model_results_service():
    return get_all_model_results()

def update_model_result_service(model_result_id, model_result_details: ModelResultUpdationDto):
    if not has_student_id(model_result_details.student_id):
        raise ValueError("Specified student_id is not currently available.") 
    existing_model_result = get_model_result(model_result_id)
    for key, value in model_result_details.__dict__.items():
        setattr(existing_model_result, key, value)
    existing_model_result.datetimeupdated = StringUtil.current_ph_time()
    update_model_result(model_result_id, existing_model_result.__dict__)

def get_model_result_by_student_id_service(student_id):
    return get_model_result_by_student_id(student_id)
