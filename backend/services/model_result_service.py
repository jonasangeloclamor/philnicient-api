from typing import List
from backend.repositories.model_result_repository import create_model_result, get_model_result, get_all_model_results, update_model_result, get_model_result_by_student_id, get_model_result_by_student_id_and_major_category, get_model_result_by_major_category, create_multiple_model_results, update_multiple_model_results, has_model_result_id
from backend.repositories.student_repository import has_student_id, is_student_enrolled_in_class
from backend.repositories.class_repository import get_class_id_by_teacher_id
from backend.repositories.user_repository import is_teacher
from backend.data_components.dtos import ModelResultCreationDto, ModelResultUpdationDto
from backend.data_components.mappings import map_model_result_creation_dto_to_model
from backend.utils.string_util import StringUtil

def create_multiple_model_results_service(model_results_details: List[ModelResultCreationDto]):
    for model_result_details in model_results_details:
        if not has_student_id(model_result_details.student_id):
            raise ValueError("Specified student_id is not currently available.")
        
        teacher_id = model_result_details.teacher_id
        class_id = get_class_id_by_teacher_id(teacher_id)
        if not class_id:
            raise ValueError("Specified teacher_id is not associated with any class.")
    
        if not is_student_enrolled_in_class(model_result_details.student_id, class_id):
            raise ValueError("Specified student_id is not enrolled in the class taught by the specified teacher.")

    existing_major_categories = set()
    for model_result_details in model_results_details:
        student_id = model_result_details.student_id
        major_category = model_result_details.major_category
        existing_result = get_model_result_by_student_id_and_major_category(student_id, major_category)
        if existing_result:
            existing_major_categories.add(major_category)

    if existing_major_categories:
        existing_major_categories_str = ', '.join(map(str, existing_major_categories))
        raise ValueError(f"Student already has results for major categories: {existing_major_categories_str}. "
                         f"Cannot add duplicate results.")

    model_results = [map_model_result_creation_dto_to_model(details) for details in model_results_details]
    model_result_ids = create_multiple_model_results(model_results)
    return model_result_ids

def update_multiple_model_results_service(model_results_details):
    missing_model_result_ids = set()
    invalid_student_ids = set()
    invalid_teacher_ids = set()

    for model_result_data in model_results_details:
        model_result_id = model_result_data.get("id")
        if not has_model_result_id(model_result_id):
            missing_model_result_ids.add(model_result_id)

    if missing_model_result_ids:
        if len(missing_model_result_ids) == 1:
            missing_model_result_id = missing_model_result_ids.pop()
            raise ValueError(f"Model Result ID '{missing_model_result_id}' is not currently available.")
        else:
            missing_model_result_ids_str = ', '.join(missing_model_result_ids)
            raise ValueError(f"The following model result IDs are not currently available: {missing_model_result_ids_str}.")

    for model_result_data in model_results_details:
        student_id = model_result_data.get("student_id")
        if not has_student_id(student_id):
            invalid_student_ids.add(student_id)

    if invalid_student_ids:
        if len(invalid_student_ids) == 1:
            invalid_student_id = invalid_student_ids.pop()
            raise ValueError(f"Student ID '{invalid_student_id}' is not valid.")
        else:
            invalid_student_ids_str = ', '.join(invalid_student_ids)
            raise ValueError(f"The following student IDs are not valid: {invalid_student_ids_str}.")

    for model_result_data in model_results_details:
        teacher_id = model_result_data.get("teacher_id")
        if not is_teacher(teacher_id):
            invalid_teacher_ids.add(teacher_id)

    if invalid_teacher_ids:
        if len(invalid_teacher_ids) == 1:
            invalid_teacher_id = invalid_teacher_ids.pop()
            raise ValueError(f"Teacher ID '{invalid_teacher_id}' is not valid.")
        else:
            invalid_teacher_ids_str = ', '.join(invalid_teacher_ids)
            raise ValueError(f"The following teacher IDs are not valid: {invalid_teacher_ids_str}.")

    current_time = StringUtil.current_ph_time()
    for model_result_data in model_results_details:
        model_result_data['datetimeupdated'] = current_time

    update_multiple_model_results(model_results_details)

def create_model_result_service(model_result_details: ModelResultCreationDto):
    if not has_student_id(model_result_details.student_id):
        raise ValueError("Specified student_id is not currently available.")
    
    teacher_id = model_result_details.teacher_id
    class_id = get_class_id_by_teacher_id(teacher_id)
    if not class_id:
        raise ValueError("Specified teacher_id is not associated with any class.")
    
    if not is_student_enrolled_in_class(model_result_details.student_id, class_id):
        raise ValueError("Specified student_id is not enrolled in the class taught by the specified teacher.")

    student_id = model_result_details.student_id
    major_category = model_result_details.major_category
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

    teacher_id = model_result_details.teacher_id
    class_id = get_class_id_by_teacher_id(teacher_id)
    if not class_id:
        raise ValueError("Specified teacher_id is not associated with any class.")

    existing_model_result = get_model_result(model_result_id)
    
    if teacher_id != existing_model_result.teacher_id:
        raise ValueError("Unauthorized to modify model result.")

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
