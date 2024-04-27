from backend.repositories.question_repository import create_questions, get_question, get_all_questions, update_question, delete_question, update_multiple_questions, has_question_id
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

def update_multiple_questions_service(question_data_list):
    missing_question_ids = set()
    missing_assessment_ids = set()
    
    for question_data in question_data_list:
        question_id = question_data.get("id")
        assessment_id = question_data.get("assessment_id")
        
        if not has_question_id(question_id):
            missing_question_ids.add(question_id)
        
        if not has_assessment_id(assessment_id):
            missing_assessment_ids.add(assessment_id)
    
    if missing_question_ids:
        if len(missing_question_ids) == 1:
            missing_question_id = missing_question_ids.pop()
            raise ValueError(f"Question ID '{missing_question_id}' is not currently available.")
        else:
            missing_question_ids_str = ', '.join(missing_question_ids)
            raise ValueError(f"The following question IDs are not currently available: {missing_question_ids_str}.")
    
    if missing_assessment_ids:
        if len(missing_assessment_ids) == 1:
            missing_assessment_id = missing_assessment_ids.pop()
            raise ValueError(f"Assessment ID '{missing_assessment_id}' is not currently available.")
        else:
            missing_assessment_ids_str = ', '.join(missing_assessment_ids)
            raise ValueError(f"The following assessment IDs are not currently available: {missing_assessment_ids_str}.")
    
    current_time = StringUtil.current_ph_time()
    for question_data in question_data_list:
        question_data['datetimeupdated'] = current_time

    update_multiple_questions(question_data_list)

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
