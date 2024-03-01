from backend.repositories.class_repository import create_class, get_class, get_all_classes, update_class, delete_class, get_class_by_code
from backend.repositories.user_repository import is_teacher
from backend.data_components.dtos import ClassCreationDto, ClassUpdationDto
from backend.data_components.mappings import map_class_creation_dto_to_model
from backend.utils.string_util import StringUtil

def create_class_service(class_data: ClassCreationDto):
    if not is_teacher(class_data.teacher_id):
        raise ValueError("Specified teacher_id does not belong to a role of teacher.")   
    class_instance = map_class_creation_dto_to_model(class_data)
    class_id, class_code = create_class(class_instance)
    class_instance.id = class_id
    class_instance.classcode = class_code
    return class_instance

def get_class_service(class_id):
    return get_class(class_id)

def get_all_classes_service():
    return get_all_classes()

def update_class_service(class_id, class_data: ClassUpdationDto):
    if not is_teacher(class_data.teacher_id):
        raise ValueError("Specified teacher_id does not belong to a role of teacher.")
    existing_class = get_class(class_id)
    for key, value in class_data.__dict__.items():
        setattr(existing_class, key, value)
    existing_class.datetimeupdated = StringUtil.current_ph_time()
    update_class(class_id, existing_class.__dict__)

def delete_class_service(class_id):
    return delete_class(class_id)

def get_class_by_code_service(class_code):
    return get_class_by_code(class_code)
