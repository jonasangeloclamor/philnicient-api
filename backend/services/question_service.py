from backend.repositories.question_repository import create_questions, get_question, get_all_questions, update_question, delete_question
from backend.repositories.assessment_repository import has_assessment_id, get_assessment, update_assessment
from backend.data_components.dtos import QuestionCreationDto, QuestionUpdationDto
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

def get_question_service(question_id):
    return get_question(question_id)

def get_all_questions_service():
    return get_all_questions()

def update_question_service(question_id, question_data: QuestionUpdationDto):
    if not has_assessment_id(question_data.assessment_id):
        raise ValueError("Specified assessment_id is not currently available.") 
 
    existing_question = get_question(question_id)
    if not existing_question:
        raise ValueError("Question with the specified ID does not exist.")
    
    old_assessment_id = existing_question.assessment_id
    
    if old_assessment_id:
        old_assessment = get_assessment(old_assessment_id)
        if old_assessment:
            old_assessment.questions = [qid for qid in old_assessment.questions if qid != question_id]
            update_assessment(old_assessment_id, old_assessment.__dict__)
    
    for key, value in question_data.__dict__.items():
        setattr(existing_question, key, value)
    existing_question.datetimeupdated = StringUtil.current_ph_time()
    existing_question.assessment_id = question_data.assessment_id
    
    update_question(question_id, existing_question.__dict__)
    
    new_assessment = get_assessment(question_data.assessment_id)
    if not new_assessment:
        raise ValueError("New assessment with the specified ID does not exist.")
    
    if question_id not in new_assessment.questions:
        new_assessment.questions.append(question_id)
    
    update_assessment(question_data.assessment_id, new_assessment.__dict__)

def delete_question_service(question_id):
    question = get_question(question_id)
    
    if question.assessment_id:
        assessment = get_assessment(question.assessment_id)
        if assessment:
            assessment.questions = [qid for qid in assessment.questions if qid != question_id]
            update_assessment(question.assessment_id, assessment.__dict__)
    
    delete_question(question_id)
