from flask import request
from flask_restx import Namespace, Resource, fields
from backend.services.question_service import create_multiple_questions_service, get_question_service, get_all_questions_service, update_question_service, delete_question_service, update_multiple_questions_service
from backend.data_components.dtos import QuestionUpdationDto
from security_config import authorizations
from backend.utils.auth import role_required

question_ns = Namespace('Question', path='/api/questions', description='Operations related to Questions', authorizations=authorizations)

question_model = question_ns.model('QuestionCreationDto', {
    'question': fields.String(required=True, description='Question'),
    'figure': fields.String(required=True, description='Figure'),
    'choices': fields.List(fields.String(), required=True, description='Choices'),
    'answer': fields.String(required=True, description='Answer'),
    'major_category': fields.String(required=True, description='Major Category'),
    'student_answer': fields.String(required=True, description='Student Answer'),
    'student_cri': fields.String(required=True, description='Student CRI'),
    'is_for_review': fields.String(required=True, description='Is For Review'),
    'time': fields.Integer(required=True, description='Time'),
    'assessment_id': fields.String(required=True, description='Assessment ID')
})

update_question_model = question_ns.model('QuestionUpdationDto', {
    'id': fields.String(required=True, description='Question ID'),
    'question': fields.String(required=True, description='Question'),
    'figure': fields.String(required=True, description='Figure'),
    'choices': fields.List(fields.String(), required=True, description='Choices'),
    'answer': fields.String(required=True, description='Answer'),
    'major_category': fields.String(required=True, description='Major Category'),
    'student_answer': fields.String(required=True, description='Student Answer'),
    'student_cri': fields.String(required=True, description='Student CRI'),
    'is_for_review': fields.String(required=True, description='Is For Review'),
    'time': fields.Integer(required=True, description='Time'),
    'assessment_id': fields.String(required=True, description='Assessment ID')
})

@question_ns.route('')
class QuestionList(Resource):
    @question_ns.expect([question_model])
    @question_ns.response(201, 'Created')
    @question_ns.response(500, 'Internal Server Error')
    @role_required('Student')
    @question_ns.doc(security="jsonWebToken")
    def post(self):
        """
        Creates multiple questions.
        """
        try:
            question_data_list = request.json
            question_ids = create_multiple_questions_service(question_data_list)
            return {'message': 'Questions created successfully', 'question_ids': question_ids}, 201
        except Exception as e:
            return {'message': str(e)}, 500

    @question_ns.response(200, 'Success')
    @question_ns.response(204, 'No Content')
    @question_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Student')
    @question_ns.doc(security="jsonWebToken")
    def get(self):
        """
        Gets all questions.
        """
        try:
            questions = get_all_questions_service()
            if questions:
                return [qt.__dict__ for qt in questions], 200
            else:
                return {'message': 'No questions found'}, 204
        except Exception as e:
            return {'message': str(e)}, 500

@question_ns.route('/update-multiple-questions')
class UpdateMultipleQuestions(Resource):
    @question_ns.expect([update_question_model])
    @question_ns.response(200, 'Success')
    @question_ns.response(500, 'Internal Server Error')
    @role_required('Student')
    @question_ns.doc(security="jsonWebToken")
    def put(self):
        """
        Updates multiple questions.
        """
        try:
            question_data_list = request.json
            update_multiple_questions_service(question_data_list)
            return {'message': 'Questions updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

@question_ns.route('/<string:question_id>')
class Question(Resource):
    @question_ns.response(200, 'Success')
    @question_ns.response(404, 'Not Found')
    @question_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Student')
    @question_ns.doc(security="jsonWebToken")
    def get(self, question_id):
        """
        Gets question details by ID.
        """
        try:
            question = get_question_service(question_id)
            if question:
                return question.__dict__, 200
            else:
                return {'message': 'Question not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

    @question_ns.expect(update_question_model)
    @question_ns.response(200, 'Success')
    @question_ns.response(404, 'Not Found')
    @question_ns.response(500, 'Internal Server Error')
    @role_required('Student')
    @question_ns.doc(security="jsonWebToken")
    def put(self, question_id):
        """
        Updates question details by ID.
        """
        try:
            if not request.json or any(value == "" for value in request.json.values()):
                return {'message': 'Request body cannot be empty or contain empty values'}, 400

            question_data = QuestionUpdationDto(**request.json)           
            question = get_question_service(question_id)           
            if not question:
                return {'message': 'Question not found'}, 404

            update_question_service(question_id, question_data)
            return {'message': 'Question updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500
    
    @question_ns.response(200, 'Success')
    @question_ns.response(404, 'Not Found')
    @question_ns.response(500, 'Internal Server Error')  
    @role_required('Teacher')
    @question_ns.doc(security="jsonWebToken")
    def delete(self, question_id):
        """
        Deletes question details by ID.
        """
        try:
            question = get_question_service(question_id)
            if not question:
                return {'message': 'Question not found'}, 404

            delete_question_service(question_id)
            return {'message': 'Question deleted successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500
        