from flask import request
from flask_restx import Namespace, Resource, fields
from backend.services.student_service import create_student_service, get_student_service, get_all_students_service, delete_student_service, get_students_by_class_id_service, is_student_in_class_service
from backend.services.assessment_service import is_assessment_for_student_service, get_assessment_service
from backend.services.class_service import get_class_service
from backend.services.user_service import check_if_user_is_student_service
from backend.data_components.dtos import StudentCreationDto
from security_config import authorizations
from flask_jwt_extended import jwt_required

student_ns = Namespace('Student', path='/api/students', description='Operations related to Students', authorizations=authorizations)

student_model = student_ns.model('StudentCreationDto', {
    'class_id': fields.String(required=True, description='Class ID'),
    'student_id': fields.String(required=True, description='Student ID')
})

@student_ns.route('')
class StudentList(Resource):
    @student_ns.expect(student_model)
    @student_ns.response(201, 'Created')
    @student_ns.response(500, 'Internal Server Error')
    def post(self):
        """
        Creates a new student.
        """
        try:
            student_data = StudentCreationDto(**request.json)
            student = create_student_service(student_data)
            return student.__dict__, 201
        except Exception as e:
            return {'message': str(e)}, 500

    @student_ns.response(200, 'Success')
    @student_ns.response(204, 'No Content')
    @student_ns.response(500, 'Internal Server Error')    
    def get(self):
        """
        Gets all students.
        """
        try:
            students = get_all_students_service()
            if students:
                return [sts.__dict__ for sts in students], 200
            else:
                return {'message': 'No students found'}, 204
        except Exception as e:
            return {'message': str(e)}, 500

@student_ns.route('/classes/<string:class_id>')
class StudentByClass(Resource):
    @student_ns.response(200, 'Success')
    @student_ns.response(204, 'No Content')
    @student_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @student_ns.doc(security="jsonWebToken")    
    def get(self, class_id):
        """
        Gets all students by class ID.
        """
        try:
            students = get_students_by_class_id_service(class_id)
            if students:
                return [sts.__dict__ for sts in students], 200
            else:
                return {'message': 'No students found for the given class ID'}, 204
        except Exception as e:
            return {'message': str(e)}, 500

@student_ns.route('/<string:student_id>')
class Student(Resource):
    @student_ns.response(200, 'Success')
    @student_ns.response(404, 'Not Found')
    @student_ns.response(500, 'Internal Server Error')
    def get(self, student_id):
        """
        Gets student details by ID.
        """
        try:
            student = get_student_service(student_id)
            if student:
                return student.__dict__, 200
            else:
                return {'message': 'Student not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

    @student_ns.response(200, 'Success')
    @student_ns.response(404, 'Not Found')
    @student_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @student_ns.doc(security="jsonWebToken")
    def delete(self, student_id):
        """
        Deletes student details by ID.
        """
        try:
            student = get_student_service(student_id)
            if student:
                delete_student_service(student_id)
                return {'message': 'Student deleted successfully'}, 200
            else:
                return {'message': 'Student not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
        
@student_ns.route('/<string:user_id>/class/<string:class_id>')
class StudentClass(Resource):
    @student_ns.response(200, 'Success')
    @student_ns.response(401, 'Unauthorized')
    @student_ns.response(404, 'Not Found')
    @student_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @student_ns.doc(security="jsonWebToken")
    def get(self, user_id, class_id):
        """
        Checks if the student with the specified user ID belongs to the class.
        """
        try:
            student = check_if_user_is_student_service(user_id)
            if not student:
                return {'message': 'Student not found'}, 404

            class_info = get_class_service(class_id)
            if not class_info:
                return {'message': 'Class not found'}, 404

            if is_student_in_class_service(user_id, class_id):
                return {'message': 'Student belongs to this class'}, 200
            else:
                return {'message': 'Student does not belong to this class'}, 401
            
        except ValueError as e:
            return {'message': str(e)}, 404
        
        except Exception as e:
            return {'message': str(e)}, 500

@student_ns.route('/<string:user_id>/assessment/<string:assessment_id>')
class StudentAssessment(Resource):
    @student_ns.response(200, 'Success')
    @student_ns.response(401, 'Unauthorized')
    @student_ns.response(404, 'Not Found')
    @student_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @student_ns.doc(security="jsonWebToken")
    def get(self, user_id, assessment_id):
        """
        Checks if the assessment is for the student with the specified user ID.
        """
        try:
            student = check_if_user_is_student_service(user_id)
            if not student:
                return {'message': 'Student not found'}, 404

            assessment_info = get_assessment_service(assessment_id)
            if not assessment_info:
                return {'message': 'Assessment not found'}, 404

            if is_assessment_for_student_service(assessment_id, user_id):
                return {'message': 'Assessment is for this student'}, 200
            else:
                return {'message': 'Assessment is not for this student'}, 401
            
        except ValueError as e:
            return {'message': str(e)}, 404
        
        except Exception as e:
            return {'message': str(e)}, 500
        