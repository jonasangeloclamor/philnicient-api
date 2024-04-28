from flask import request
from flask_restx import Namespace, Resource, fields
from backend.services.class_service import create_class_service, get_class_service, get_all_classes_service, update_class_service, delete_class_service, get_class_by_code_service
from backend.data_components.dtos import ClassCreationDto, ClassUpdationDto
from security_config import authorizations
from backend.utils.auth import role_required

class_ns = Namespace('Class', path='/api/classes', description='Operations related to Classes', authorizations=authorizations)

class_model = class_ns.model('ClassCreationDto', {
    'classname': fields.String(required=True, description='Class Name'),
    'teacher_id': fields.String(required=True, description='Teacher ID')
})

update_class_model = class_ns.model('ClassUpdationDto', {
    'classname': fields.String(required=True, description='Class Name'),
    'teacher_id': fields.String(required=True, description='Teacher ID')
})

@class_ns.route('')
class ClassList(Resource):
    @class_ns.expect(class_model)
    @class_ns.response(201, 'Created')
    @class_ns.response(500, 'Internal Server Error')
    @role_required('Teacher')
    @class_ns.doc(security="jsonWebToken")
    def post(self):
        """
        Creates a new class.
        """
        try:
            class_data = ClassCreationDto(**request.json)
            class_instance = create_class_service(class_data)
            return {'id': class_instance.id, 'classcode': class_instance.classcode}, 201
        except Exception as e:
            return {'message': str(e)}, 500

    @class_ns.response(200, 'Success')
    @class_ns.response(204, 'No Content')
    @class_ns.response(500, 'Internal Server Error')
    @role_required('Admin', 'Teacher', 'Student')
    @class_ns.doc(security="jsonWebToken")    
    def get(self):
        """
        Gets all classes.
        """
        try:
            classes = get_all_classes_service()
            if classes:
                return [cls.__dict__ for cls in classes], 200
            else:
                return {'message': 'No classes found'}, 204
        except Exception as e:
            return {'message': str(e)}, 500

@class_ns.route('/<string:class_id>')
class Class(Resource):
    @class_ns.response(200, 'Success')
    @class_ns.response(404, 'Not Found')
    @class_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Student', 'Admin')
    @class_ns.doc(security="jsonWebToken")
    def get(self, class_id):
        """
        Gets class details by ID.
        """
        try:
            class_instance = get_class_service(class_id)
            if class_instance:
                return class_instance.__dict__, 200
            else:
                return {'message': 'Class not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

    @class_ns.expect(update_class_model)
    @class_ns.response(200, 'Success')
    @class_ns.response(400, 'Bad Request')
    @class_ns.response(404, 'Not Found')
    @class_ns.response(500, 'Internal Server Error')
    @role_required('Teacher')
    @class_ns.doc(security="jsonWebToken")
    def put(self, class_id):
        """
        Updates class details by ID.
        """
        try:
            if not request.json or any(value == "" for value in request.json.values()):
                return {'message': 'Request body cannot be empty or contain empty values'}, 400

            class_data = ClassUpdationDto(**request.json)           
            class_instance = get_class_service(class_id)           
            if not class_instance:
                return {'message': 'Class not found'}, 404

            update_class_service(class_id, class_data)
            return {'message': 'Class updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

    @class_ns.response(200, 'Success')
    @class_ns.response(404, 'Not Found')
    @class_ns.response(500, 'Internal Server Error')
    @role_required('Admin')
    @class_ns.doc(security="jsonWebToken")
    def delete(self, class_id):
        """
        Deletes class details by ID.
        """
        try:
            class_instance = get_class_service(class_id)
            if class_instance:
                delete_class_service(class_id)
                return {'message': 'Class deleted successfully'}, 200
            else:
                return {'message': 'Class not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

@class_ns.route('/code/<string:class_code>')
class ClassByCode(Resource):
    @class_ns.response(200, 'Success')
    @class_ns.response(404, 'Not Found')
    @class_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Student')
    @class_ns.doc(security="jsonWebToken")
    def get(self, class_code):
        """
        Gets class details by class code.
        """
        try:
            class_instance = get_class_by_code_service(class_code)
            if class_instance:
                return class_instance.__dict__, 200
            else:
                return {'message': 'Class not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
        