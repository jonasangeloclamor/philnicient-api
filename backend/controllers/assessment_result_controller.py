from flask import request
from flask_restx import Namespace, Resource, fields
from backend.services.assessment_result_service import create_assessment_result_service, get_assessment_result_service, get_all_assessment_results_service, update_assessment_result_service, get_assessment_result_by_student_id_service, delete_assessment_result_service
from backend.data_components.dtos import AssessmentResultCreationDto, AssessmentResultUpdationDto
from security_config import authorizations
from backend.utils.auth import role_required

assessment_result_ns = Namespace('AssessmentResult', path='/api/assessment_results', description='Operations related to Assessment Results', authorizations=authorizations)

assessment_result_model = assessment_result_ns.model('AssessmentResultCreationDto', {
    'total_items': fields.Integer(required=True, description='Total Items'),
    'total_score': fields.Integer(required=True, description='Total Score'),
    'basic_theory_score': fields.Integer(required=True, description='Basic Theory Score'),
    'computer_systems_score': fields.Integer(required=True, description='Computer Systems Score'),
    'technical_elements_score': fields.Integer(required=True, description='Technical Elements Score'),
    'development_techniques_score': fields.Integer(required=True, description='Development Techniques Score'),
    'project_management_score': fields.Integer(required=True, description='Project Management Score'),
    'service_management_score': fields.Integer(required=True, description='Service Management Score'),
    'system_strategy_score': fields.Integer(required=True, description='System Strategy Score'),
    'management_strategy_score': fields.Integer(required=True, description='Management Strategy Score'),
    'corporate_legal_affairs_score': fields.Integer(required=True, description='Corporate Legal Affairs Score'),
    'student_id': fields.String(required=True, description='Student ID'),
    'teacher_id': fields.String(required=True, description='Teacher ID')
})

update_assessment_result_model = assessment_result_ns.model('AssessmentResultUpdationDto', {
    'total_items': fields.Integer(required=True, description='Total Items'),
    'total_score': fields.Integer(required=True, description='Total Score'),
    'basic_theory_score': fields.Integer(required=True, description='Basic Theory Score'),
    'computer_systems_score': fields.Integer(required=True, description='Computer Systems Score'),
    'technical_elements_score': fields.Integer(required=True, description='Technical Elements Score'),
    'development_techniques_score': fields.Integer(required=True, description='Development Techniques Score'),
    'project_management_score': fields.Integer(required=True, description='Project Management Score'),
    'service_management_score': fields.Integer(required=True, description='Service Management Score'),
    'system_strategy_score': fields.Integer(required=True, description='System Strategy Score'),
    'management_strategy_score': fields.Integer(required=True, description='Management Strategy Score'),
    'corporate_legal_affairs_score': fields.Integer(required=True, description='Corporate Legal Affairs Score'),
    'student_id': fields.String(required=True, description='Student ID'),
    'teacher_id': fields.String(required=True, description='Teacher ID')
})

@assessment_result_ns.route('')
class AssessmentResultList(Resource):
    @assessment_result_ns.expect(assessment_result_model)
    @assessment_result_ns.response(201, 'Created')
    @assessment_result_ns.response(400, 'Bad Request')
    @assessment_result_ns.response(500, 'Internal Server Error')
    @role_required('Teacher')
    @assessment_result_ns.doc(security="jsonWebToken")
    def post(self):
        """
        Creates a new assessment result.
        """
        try:
            assessment_result_details = AssessmentResultCreationDto(**request.json)
            assessment_result = create_assessment_result_service(assessment_result_details)
            return assessment_result.__dict__, 201
        except ValueError as ve:
            return {'message': str(ve)}, 400
        except Exception as e:
            return {'message': str(e)}, 500

    @assessment_result_ns.response(200, 'Success')
    @assessment_result_ns.response(204, 'No Content')
    @assessment_result_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Student', 'Admin')
    @assessment_result_ns.doc(security="jsonWebToken")  
    def get(self):
        """
        Gets all assessment results.
        """
        try:
            assessment_results = get_all_assessment_results_service()
            if assessment_results:
                return [rst.__dict__ for rst in assessment_results], 200
            else:
                return {'message': 'No assessment results found'}, 204
        except Exception as e:
            return {'message': str(e)}, 500

@assessment_result_ns.route('/<string:assessment_result_id>')
class AssessmentResult(Resource):
    @assessment_result_ns.response(200, 'Success')
    @assessment_result_ns.response(404, 'Not Found')
    @assessment_result_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Student', 'Admin')
    @assessment_result_ns.doc(security="jsonWebToken")
    def get(self, assessment_result_id):
        """
        Gets assessment result details by ID.
        """
        try:
            assessment_result = get_assessment_result_service(assessment_result_id)
            if assessment_result:
                return assessment_result.__dict__, 200
            else:
                return {'message': 'Assessment result not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
    
    @assessment_result_ns.expect(update_assessment_result_model)
    @assessment_result_ns.response(200, 'Success')
    @assessment_result_ns.response(400, 'Bad Request')
    @assessment_result_ns.response(404, 'Not Found')
    @assessment_result_ns.response(500, 'Internal Server Error')
    @role_required('Teacher')
    @assessment_result_ns.doc(security="jsonWebToken")
    def put(self, assessment_result_id):
        """
        Updates assessment result details by ID.
        """
        try:
            if not request.json or any(value == "" for value in request.json.values()):
                return {'message': 'Request body cannot be empty or contain empty values'}, 400

            assessment_result_details = AssessmentResultUpdationDto(**request.json)           
            assessment_result = get_assessment_result_service(assessment_result_id)           
            if not assessment_result:
                return {'message': 'Assessment result not found'}, 404

            update_assessment_result_service(assessment_result_id, assessment_result_details)
            return {'message': 'Assessment result updated successfully'}, 200
        except ValueError as ve:
            return {'message': str(ve)}, 400
        except Exception as e:
            return {'message': str(e)}, 

    @assessment_result_ns.response(200, 'Success')
    @assessment_result_ns.response(404, 'Not Found')
    @assessment_result_ns.response(500, 'Internal Server Error')
    @role_required('Teacher')
    @assessment_result_ns.doc(security="jsonWebToken")
    def delete(self, assessment_result_id):
        """
        Deletes assessment result details by ID.
        """
        try:
            assessment_result = get_assessment_result_service(assessment_result_id) 
            if assessment_result:
                delete_assessment_result_service(assessment_result_id)
                return {'message': 'Assessment result deleted successfully'}, 200
            else:
                return {'message': 'Assessment result not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

@assessment_result_ns.route('/students/<string:student_id>')
class AssessmentResultByStudent(Resource):
    @assessment_result_ns.response(200, 'Success')
    @assessment_result_ns.response(404, 'Not Found')
    @assessment_result_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Student', 'Admin')
    @assessment_result_ns.doc(security="jsonWebToken")
    def get(self, student_id):
        """
        Gets assessment result details by student ID.
        """
        try:
            assessment_result = get_assessment_result_by_student_id_service(student_id)
            if assessment_result:
                return assessment_result.__dict__, 200
            else:
                return {'message': 'Assessment result not found for the specified student'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
