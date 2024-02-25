from flask import request
from flask_restx import Namespace, Resource, fields
from backend.services.student_assessment_service import create_student_assessment_service, get_student_assessment_service, get_all_student_assessments_service, update_student_assessment_service
from backend.data_components.dtos import StudentAssessmentCreationDto, StudentAssessmentUpdationDto
from security_config import authorizations
from flask_jwt_extended import jwt_required

student_assessment_ns = Namespace('StudentAssessment', path='/api/student_assessments', description='Operations related to StudentAssessments', authorizations=authorizations)

student_assessment_model = student_assessment_ns.model('StudentAssessmentCreationDto', {
    'student_id': fields.String(required=True, description='Student ID')
})

update_student_assessment_model = student_assessment_ns.model('StudentAssessmentUpdationDto', {
    'student_id': fields.String(required=True, description='Student ID')
})

@student_assessment_ns.route('')
class StudentAssessmentList(Resource):
    @student_assessment_ns.expect(student_assessment_model)
    @student_assessment_ns.response(201, 'Created')
    @student_assessment_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @student_assessment_ns.doc(security="jsonWebToken")
    def post(self):
        """
        Creates a new student assessment.
        """
        try:
            student_assessment_data = StudentAssessmentCreationDto(**request.json)
            student_assessment = create_student_assessment_service(student_assessment_data)
            return student_assessment.__dict__, 201
        except Exception as e:
            return {'message': str(e)}, 500

    @student_assessment_ns.response(200, 'Success')
    @student_assessment_ns.response(204, 'No Content')
    @student_assessment_ns.response(500, 'Internal Server Error')  
    def get(self):
        """
        Gets all student assessments.
        """
        try:
            student_assessments = get_all_student_assessments_service()
            if student_assessments:
                return [sa.__dict__ for sa in student_assessments], 200
            else:
                return {'message': 'No student assessments found'}, 204
        except Exception as e:
            return {'message': str(e)}, 500

@student_assessment_ns.route('/<string:student_assessment_id>')
class StudentAssessment(Resource):
    @student_assessment_ns.response(200, 'Success')
    @student_assessment_ns.response(404, 'Not Found')
    @student_assessment_ns.response(500, 'Internal Server Error')
    def get(self, student_assessment_id):
        """
        Gets student assessment details by ID.
        """
        try:
            student_assessment = get_student_assessment_service(student_assessment_id)
            if student_assessment:
                return student_assessment.__dict__, 200
            else:
                return {'message': 'Student assessment not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

    @student_assessment_ns.expect(update_student_assessment_model)
    @student_assessment_ns.response(200, 'Success')
    @student_assessment_ns.response(404, 'Not Found')
    @student_assessment_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @student_assessment_ns.doc(security="jsonWebToken")
    def put(self, student_assessment_id):
        """
        Updates student assessment details by ID.
        """
        try:
            if not request.json or any(value == "" for value in request.json.values()):
                return {'message': 'Request body cannot be empty or contain empty values'}, 400

            student_assessment_data = StudentAssessmentUpdationDto(**request.json)           
            student_assessment = get_student_assessment_service(student_assessment_id)           
            if not student_assessment:
                return {'message': 'Student assessment not found'}, 404

            update_student_assessment_service(student_assessment_id, student_assessment_data)
            return {'message': 'Student assessment updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500
        