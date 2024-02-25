from backend.repositories.assessment_repository import create_assessment, get_assessment, get_all_assessments, update_assessment
from backend.repositories.student_assessment_repository import has_student_assessment_id, create_student_assessment, get_student_assessment, update_student_assessment
from backend.data_components.models import StudentAssessment
from backend.data_components.dtos import AssessmentCreationDto, AssessmentUpdationDto
from backend.data_components.mappings import map_assessment_creation_dto_to_model
from backend.utils.string_util import StringUtil

def create_assessment_service(assessment_data: AssessmentCreationDto):
    if not has_student_assessment_id(assessment_data.student_assessment_id):
        raise ValueError("Specified student_assessment_id is not currently available.")

    assessment = map_assessment_creation_dto_to_model(assessment_data)
    assessment_id = create_assessment(assessment)
    assessment.id = assessment_id
    
    student_assessment_id = assessment_data.student_assessment_id
    student_assessment = get_student_assessment(student_assessment_id)
    if student_assessment:
        student_assessment.assessments.append(assessment_id)
        update_student_assessment(student_assessment_id, student_assessment.__dict__)
    
    return assessment

def get_assessment_service(assessment_id):
    return get_assessment(assessment_id)

def get_all_assessments_service():
    return get_all_assessments()

def update_assessment_service(assessment_id, assessment_data: AssessmentUpdationDto):
    if not has_student_assessment_id(assessment_data.student_assessment_id):
        raise ValueError("Specified student_assessment_id is not currently available.") 
    existing_assessment = get_assessment(assessment_id)
    for key, value in assessment_data.__dict__.items():
        setattr(existing_assessment, key, value)
    existing_assessment.datetimeupdated = StringUtil.get_current_datetime()
    update_assessment(assessment_id, existing_assessment.__dict__)
