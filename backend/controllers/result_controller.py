from flask import request
from flask_restx import Namespace, Resource, fields
from backend.services.result_service import create_result_service, get_result_service, get_all_results_service, update_result_service, get_result_by_student_id_service
from backend.data_components.dtos import ResultCreationDto, ResultUpdationDto
from security_config import authorizations
from flask_jwt_extended import jwt_required

result_ns = Namespace('Result', path='/api/results', description='Operations related to Results', authorizations=authorizations)

result_model = result_ns.model('ResultCreationDto', {
    'major_category': fields.String(required=True, description='Major Category'),
    'number_of_items': fields.Integer(required=True, description='Number of Items'),
    'total_score': fields.Integer(required=True, description='Total Score'),
    'total_time_taken': fields.Integer(required=True, description='Total Time Taken'),
    'average_cri': fields.Float(required=True, description='Average CRI'),
    'cri_criteria': fields.String(required=True, description='CRI Criteria'),
    'student_id': fields.String(required=True, description='Student ID')
})

update_result_model = result_ns.model('ResultUpdationDto', {
    'major_category': fields.String(required=True, description='Major Category'),
    'number_of_items': fields.Integer(required=True, description='Number of Items'),
    'total_score': fields.Integer(required=True, description='Total Score'),
    'total_time_taken': fields.Integer(required=True, description='Total Time Taken'),
    'average_cri': fields.Float(required=True, description='Average CRI'),
    'cri_criteria': fields.String(required=True, description='CRI Criteria'),
    'student_id': fields.String(required=True, description='Student ID')
})

@result_ns.route('')
class ResultList(Resource):
    @result_ns.expect(result_model)
    @result_ns.response(201, 'Created')
    @result_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @result_ns.doc(security="jsonWebToken")
    def post(self):
        """
        Creates a new result.
        """
        try:
            result_details = ResultCreationDto(**request.json)
            result = create_result_service(result_details)
            return result.__dict__, 201
        except Exception as e:
            return {'message': str(e)}, 500

    @result_ns.response(200, 'Success')
    @result_ns.response(204, 'No Content')
    @result_ns.response(500, 'Internal Server Error')    
    def get(self):
        """
        Gets all results.
        """
        try:
            results = get_all_results_service()
            if results:
                return [rst.__dict__ for rst in results], 200
            else:
                return {'message': 'No results found'}, 204
        except Exception as e:
            return {'message': str(e)}, 500

@result_ns.route('/<string:result_id>')
class Result(Resource):
    @result_ns.response(200, 'Success')
    @result_ns.response(404, 'Not Found')
    @result_ns.response(500, 'Internal Server Error')
    def get(self, result_id):
        """
        Gets result details by ID.
        """
        try:
            result = get_result_service(result_id)
            if result:
                return result.__dict__, 200
            else:
                return {'message': 'Result not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

    @result_ns.expect(update_result_model)
    @result_ns.response(200, 'Success')
    @result_ns.response(400, 'Bad Request')
    @result_ns.response(404, 'Not Found')
    @result_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @result_ns.doc(security="jsonWebToken")
    def put(self, result_id):
        """
        Updates result details by ID.
        """
        try:
            if not request.json or any(value == "" for value in request.json.values()):
                return {'message': 'Request body cannot be empty or contain empty values'}, 400

            result_details = ResultUpdationDto(**request.json)           
            result = get_result_service(result_id)           
            if not result:
                return {'message': 'Result not found'}, 404

            update_result_service(result_id, result_details)
            return {'message': 'Result updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

@result_ns.route('/students/<string:student_id>')
class ResultByStudent(Resource):
    @result_ns.response(200, 'Success')
    @result_ns.response(404, 'Not Found')
    @result_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @result_ns.doc(security="jsonWebToken")
    def get(self, student_id):
        """
        Gets result details by student ID.
        """
        try:
            result = get_result_by_student_id_service(student_id)
            if result:
                return result.__dict__, 200
            else:
                return {'message': 'Result not found for the specified student'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
