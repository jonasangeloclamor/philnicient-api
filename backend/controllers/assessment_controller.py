from flask import request
from flask_restx import Namespace, Resource, fields
from backend.services.assessment_service import create_assessment_service, get_assessment_service, get_all_assessments_service, update_assessment_service, get_assessment_id_by_student_id_service, delete_assessment_service
from backend.data_components.dtos import AssessmentCreationDto, AssessmentUpdationDto
from security_config import authorizations
from backend.utils.auth import role_required

assessment_ns = Namespace('Assessment', path='/api/assessments', description='Operations related to Assessments', authorizations=authorizations)

assessment_model = assessment_ns.model('AssessmentCreationDto', {
    'student_id': fields.String(required=True, description='Student ID')
})

update_assessment_model = assessment_ns.model('AssessmentUpdationDto', {
    'student_id': fields.String(required=True, description='Student ID')
})

@assessment_ns.route('')
class AssessmentList(Resource):
    @assessment_ns.expect(assessment_model)
    @assessment_ns.response(201, 'Created')
    @assessment_ns.response(400, 'Bad Request')
    @assessment_ns.response(500, 'Internal Server Error')
    @role_required('Student')
    @assessment_ns.doc(security="jsonWebToken")
    def post(self):
        """
        Creates a new assessment.
        """
        try:
            assessment_data = AssessmentCreationDto(**request.json)
            assessment = create_assessment_service(assessment_data)
            return assessment.__dict__, 201
        except ValueError as ve:
            return {'message': str(ve)}, 400
        except Exception as e:
            return {'message': str(e)}, 500

    @assessment_ns.response(200, 'Success')
    @assessment_ns.response(204, 'No Content')
    @assessment_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Admin')
    @assessment_ns.doc(security="jsonWebToken")
    def get(self):
        """
        Gets all assessments.
        """
        try:
            assessments = get_all_assessments_service()
            if assessments:
                return [a.__dict__ for a in assessments], 200
            else:
                return {'message': 'No assessments found'}, 204
        except Exception as e:
            return {'message': str(e)}, 500

@assessment_ns.route('/<string:assessment_id>')
class Assessment(Resource):
    @assessment_ns.response(200, 'Success')
    @assessment_ns.response(404, 'Not Found')
    @assessment_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Student', 'Admin')
    @assessment_ns.doc(security="jsonWebToken")
    def get(self, assessment_id):
        """
        Gets assessment details by ID.
        """
        try:
            assessment = get_assessment_service(assessment_id)
            if assessment:
                return assessment.__dict__, 200
            else:
                return {'message': 'Assessment not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

    @assessment_ns.expect(update_assessment_model)
    @assessment_ns.response(200, 'Success')
    @assessment_ns.response(404, 'Not Found')
    @assessment_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Admin')
    @assessment_ns.doc(security="jsonWebToken")
    def put(self, assessment_id):
        """
        Updates assessment details by ID.
        """
        try:
            if not request.json or any(value == "" for value in request.json.values()):
                return {'message': 'Request body cannot be empty or contain empty values'}, 400

            assessment_data = AssessmentUpdationDto(**request.json)           
            assessment = get_assessment_service(assessment_id)           
            if not assessment:
                return {'message': 'Assessment not found'}, 404

            update_assessment_service(assessment_id, assessment_data)
            return {'message': 'Assessment updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

    @assessment_ns.response(200, 'Success')
    @assessment_ns.response(404, 'Not Found')
    @assessment_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Admin')
    @assessment_ns.doc(security="jsonWebToken")
    def delete(self, assessment_id):
        """
        Deletes assessment details by ID.
        """
        try:
            assessment = get_assessment_service(assessment_id)
            if not assessment:
                return {'message': 'Assessment not found'}, 404

            delete_assessment_service(assessment_id)
            return {'message': 'Assessment deleted successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

@assessment_ns.route('/students/<string:student_id>')
class AssessmentByStudent(Resource):
    @assessment_ns.response(200, 'Success')
    @assessment_ns.response(404, 'Not Found')
    @assessment_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Admin')
    @assessment_ns.doc(security="jsonWebToken")
    def get(self, student_id):
        """
        Gets assessment details specifically its ID by student ID.
        """
        try:
            assessment_id = get_assessment_id_by_student_id_service(student_id)
            if assessment_id:
                return {'assessment_id': assessment_id}, 200
            else:
                return {'message': 'Assessment not found for the given student ID'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
        