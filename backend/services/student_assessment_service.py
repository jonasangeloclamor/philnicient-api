from backend.repositories.student_assessment_repository import create_student_assessment, get_student_assessment, get_all_student_assessments, update_student_assessment
from backend.repositories.student_repository import has_student_id
from backend.data_components.dtos import StudentAssessmentCreationDto, StudentAssessmentUpdationDto
from backend.data_components.mappings import map_student_assessment_creation_dto_to_model
from backend.utils.string_util import StringUtil

def create_student_assessment_service(student_assessment_data: StudentAssessmentCreationDto):
    if not has_student_id(student_assessment_data.student_id):
        raise ValueError("Specified student_id is not currently available.")
    student_assessment = map_student_assessment_creation_dto_to_model(student_assessment_data)
    student_assessment_id = create_student_assessment(student_assessment)
    student_assessment.id = student_assessment_id
    return student_assessment

def get_student_assessment_service(student_assessment_id):
    return get_student_assessment(student_assessment_id)

def get_all_student_assessments_service():
    return get_all_student_assessments()

def update_student_assessment_service(student_assessment_id, student_assessment_data: StudentAssessmentUpdationDto):
    if not has_student_id(student_assessment_data.student_id):
        raise ValueError("Specified student_id is not currently available.") 
    existing_student_assessment = get_student_assessment(student_assessment_id)
    for key, value in student_assessment_data.__dict__.items():
        setattr(existing_student_assessment, key, value)
    existing_student_assessment.datetimeupdated = StringUtil.current_ph_time()
    update_student_assessment(student_assessment_id, existing_student_assessment.__dict__)
