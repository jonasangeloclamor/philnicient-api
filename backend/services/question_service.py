from backend.repositories.question_repository import create_questions, get_question, get_all_questions, update_question, delete_question, update_multiple_questions, has_question_id, get_questions_by_assessment_id
from backend.repositories.assessment_repository import has_assessment_id, get_assessment, update_assessment
from backend.repositories.user_repository import is_teacher
from backend.data_components.dtos import QuestionCreationDto, QuestionUpdationDto, QuestionDetailsDto
from backend.data_components.mappings import map_question_creation_dto_to_model
from backend.utils.string_util import StringUtil

def create_multiple_questions_service(question_data_list):
    questions = [QuestionCreationDto(**question_data) for question_data in question_data_list]
    question_objects = [map_question_creation_dto_to_model(question_data) for question_data in questions]
    question_ids = create_questions(question_objects)

    assessment_id = question_data_list[0].get("assessment_id")

    if not has_assessment_id(assessment_id):
        raise ValueError("Specified assessment_id is not currently available.")

    if assessment_id:
        assessment = get_assessment(assessment_id)
        if assessment:
            if not assessment.questions:
                assessment.questions = question_ids
            else:
                assessment.questions.extend(question_ids)
            update_assessment(assessment_id, assessment.__dict__)

    return question_ids

def update_multiple_questions_service(question_data_list):
    missing_question_ids = set()
    
    for question_data in question_data_list:
        question_id = question_data.get("id")
        
        if not has_question_id(question_id):
            missing_question_ids.add(question_id)
    
    if missing_question_ids:
        if len(missing_question_ids) == 1:
            missing_question_id = missing_question_ids.pop()
            raise ValueError(f"Question ID '{missing_question_id}' is not currently available.")
        else:
            missing_question_ids_str = ', '.join(missing_question_ids)
            raise ValueError(f"The following question IDs are not currently available: {missing_question_ids_str}.")
    
    current_time = StringUtil.current_ph_time()
    for question_data in question_data_list:
        question_data['datetimeupdated'] = current_time

    update_multiple_questions(question_data_list)

def get_question_service(question_id):
    question = get_question(question_id)
    if question:
        question_dict = question.__dict__
        question_dict.pop('answer', None)
        return QuestionDetailsDto(**question_dict)
    else:
        return None

def get_all_questions_service():
    questions = get_all_questions()
    question_dtos = []
    for question in questions:
        question_dict = question.__dict__
        question_dict.pop('answer', None)
        question_dtos.append(QuestionDetailsDto(**question_dict))
    return question_dtos

def update_question_service(question_id, question_data: QuestionUpdationDto):
    existing_question = get_question(question_id)
    if not existing_question:
        raise ValueError("Question with the specified ID does not exist.")
    
    for key, value in question_data.__dict__.items():
        setattr(existing_question, key, value)
    existing_question.datetimeupdated = StringUtil.current_ph_time()
    
    update_question(question_id, existing_question.__dict__)

def delete_question_service(question_id):
    question = get_question(question_id)
    
    if question.assessment_id:
        assessment = get_assessment(question.assessment_id)
        if assessment:
            assessment.questions = [qid for qid in assessment.questions if qid != question_id]
            update_assessment(question.assessment_id, assessment.__dict__)
    
    delete_question(question_id)

def get_questions_by_assessment_id_service(assessment_id, user_id):
    questions = get_questions_by_assessment_id(assessment_id)
    is_teacher_user = is_teacher(user_id)

    if is_teacher_user:
        return [question.__dict__ for question in questions]
    else:
        return [{k: v for k, v in question.__dict__.items() if k != 'answer'} for question in questions]
