from backend.repositories.model_result_repository import create_model_result, get_model_result, get_all_model_results, update_model_result, get_model_result_by_student_id, get_model_result_by_student_id_and_major_category, get_number_of_model_results_for_student, get_model_result_by_major_category
from backend.repositories.student_repository import has_student_id
from backend.data_components.dtos import ModelResultCreationDto, ModelResultUpdationDto
from backend.data_components.mappings import map_model_result_creation_dto_to_model
from backend.utils.string_util import StringUtil

def create_model_result_service(model_result_details: ModelResultCreationDto):
    if not has_student_id(model_result_details.student_id):
        raise ValueError("Specified student_id is not currently available.") 

    student_id = model_result_details.student_id
    num_results = get_number_of_model_results_for_student(student_id)

    if num_results >= 9:
        raise ValueError("Student already has the maximum allowed number of model results.")

    major_category = model_result_details.major_category
    if major_category < 1 or major_category > 9:
        raise ValueError("Major category value should be between 1 and 9.")

    existing_result = get_model_result_by_student_id_and_major_category(student_id, major_category)

    if existing_result:
        raise ValueError(f"Student already has a result for major category {major_category}")

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
    if model_result_details.student_id != existing_model_result.student_id:
        raise ValueError("Cannot change student ID when updating model result.")
    
    if model_result_details.major_category != existing_model_result.major_category:
        raise ValueError("Cannot change the value of major category when updating model result.")
    
    for key, value in model_result_details.__dict__.items():
        setattr(existing_model_result, key, value)
    existing_model_result.datetimeupdated = StringUtil.current_ph_time()
    update_model_result(model_result_id, existing_model_result.__dict__)

def get_model_result_by_student_id_service(student_id):
    return get_model_result_by_student_id(student_id)

def get_model_result_by_student_id_and_major_category_service(student_id, major_category):
    return get_model_result_by_student_id_and_major_category(student_id, major_category)

def get_model_result_by_major_category_service(major_category):
    return get_model_result_by_major_category(major_category)
