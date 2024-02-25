from backend.data_components.models import User, Class, Student, Result, StudentAssessment, Assessment
from backend.data_components.dtos import UserCreationDto, ClassCreationDto, StudentCreationDto, ResultCreationDto, StudentAssessmentCreationDto, AssessmentCreationDto
from backend.utils.string_util import StringUtil

def map_user_creation_dto_to_model(dto: UserCreationDto) -> User:
    current_datetime = StringUtil.get_current_datetime()
    return User(id=None, datetimecreated=current_datetime, datetimeupdated=current_datetime, **dto.__dict__)

def map_class_creation_dto_to_model(dto: ClassCreationDto) -> Class:
    current_datetime = StringUtil.get_current_datetime()
    return Class(id=None, datetimecreated=current_datetime, datetimeupdated=current_datetime, **dto.__dict__)

def map_student_creation_dto_to_model(dto: StudentCreationDto) -> Student:
    current_datetime = StringUtil.get_current_datetime()
    return Student(id=None, datetimecreated=current_datetime, datetimeupdated=current_datetime, **dto.__dict__)

def map_result_creation_dto_to_model(dto: ResultCreationDto) -> Result:
    current_datetime = StringUtil.get_current_datetime()
    return Result(id=None, assessments=None, datetimecreated=current_datetime, datetimeupdated=current_datetime, **dto.__dict__)

def map_student_assessment_creation_dto_to_model(dto: StudentAssessmentCreationDto) -> StudentAssessment:
    current_datetime = StringUtil.get_current_datetime()
    return StudentAssessment(id=None, datetimecreated=current_datetime, datetimeupdated=current_datetime, **dto.__dict__)

def map_assessment_creation_dto_to_model(dto: AssessmentCreationDto) -> Assessment:
    current_datetime = StringUtil.get_current_datetime()
    return Assessment(id=None, datetimecreated=current_datetime, datetimeupdated=current_datetime, **dto.__dict__)
