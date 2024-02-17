from flask import request
from flask_restx import Namespace, Resource, fields
from backend.services.student_service import create_student_service, get_student_service, get_all_students_service, delete_student_service, get_students_by_class_id_service
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

@student_ns.route('/class/<string:class_id>')
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
        