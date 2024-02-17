from backend.repositories.data_repository import create_data, get_data, get_all_data, update_data, get_data_by_student_id
from backend.repositories.student_repository import has_student_id
from backend.data_components.dtos import DataCreationDto, DataUpdationDto
from backend.data_components.mappings import map_data_creation_dto_to_model
from backend.utils.string_util import StringUtil

def create_data_service(data_details: DataCreationDto):
    if not has_student_id(data_details.student_id):
        raise ValueError("Specified student_id is not currently available.") 
    data = map_data_creation_dto_to_model(data_details)
    data_id = create_data(data)
    data.id = data_id
    return data

def get_data_service(data_id):
    return get_data(data_id)

def get_all_data_service():
    return get_all_data()

def update_data_service(data_id, data_details: DataUpdationDto):
    if not has_student_id(data_details.student_id):
        raise ValueError("Specified student_id is not currently available.") 
    existing_data = get_data(data_id)
    for key, value in data_details.__dict__.items():
        setattr(existing_data, key, value)
    existing_data.datetimeupdated = StringUtil.get_current_datetime()
    update_data(data_id, existing_data.__dict__)

def get_data_by_student_id_service(student_id):
    return get_data_by_student_id(student_id)
