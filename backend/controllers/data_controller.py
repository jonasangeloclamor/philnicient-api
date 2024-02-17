from flask import request
from flask_restx import Namespace, Resource, fields
from backend.services.data_service import create_data_service, get_data_service, get_all_data_service, update_data_service, get_data_by_student_id_service
from backend.data_components.dtos import DataCreationDto, DataUpdationDto
from security_config import authorizations
from flask_jwt_extended import jwt_required

data_ns = Namespace('Data', path='/api/data', description='Operations related to Data', authorizations=authorizations)

data_model = data_ns.model('DataCreationDto', {
    'major_category': fields.String(required=True, description='Major Category'),
    'number_of_items': fields.Integer(required=True, description='Number of Items'),
    'total_score': fields.Integer(required=True, description='Total Score'),
    'total_time_taken': fields.Integer(required=True, description='Total Time Taken'),
    'average_cri': fields.Float(required=True, description='Average CRI'),
    'cri_criteria': fields.String(required=True, description='CRI Criteria'),
    'student_id': fields.String(required=True, description='Student ID')
})

update_data_model = data_ns.model('DataUpdationDto', {
    'major_category': fields.String(required=True, description='Major Category'),
    'number_of_items': fields.Integer(required=True, description='Number of Items'),
    'total_score': fields.Integer(required=True, description='Total Score'),
    'total_time_taken': fields.Integer(required=True, description='Total Time Taken'),
    'average_cri': fields.Float(required=True, description='Average CRI'),
    'cri_criteria': fields.String(required=True, description='CRI Criteria'),
    'student_id': fields.String(required=True, description='Student ID')
})

@data_ns.route('')
class DataList(Resource):
    @data_ns.expect(data_model)
    @data_ns.response(201, 'Created')
    @data_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @data_ns.doc(security="jsonWebToken")
    def post(self):
        """
        Creates a new data.
        """
        try:
            data_details = DataCreationDto(**request.json)
            data = create_data_service(data_details)
            return data.__dict__, 201
        except Exception as e:
            return {'message': str(e)}, 500

    @data_ns.response(200, 'Success')
    @data_ns.response(204, 'No Content')
    @data_ns.response(500, 'Internal Server Error')    
    def get(self):
        """
        Gets all data.
        """
        try:
            data = get_all_data_service()
            if data:
                return [dt.__dict__ for dt in data], 200
            else:
                return {'message': 'No data found'}, 204
        except Exception as e:
            return {'message': str(e)}, 500

@data_ns.route('/<string:data_id>')
class Data(Resource):
    @data_ns.response(200, 'Success')
    @data_ns.response(404, 'Not Found')
    @data_ns.response(500, 'Internal Server Error')
    def get(self, data_id):
        """
        Gets data details by ID.
        """
        try:
            data = get_data_service(data_id)
            if data:
                return data.__dict__, 200
            else:
                return {'message': 'Data not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

    @data_ns.expect(update_data_model)
    @data_ns.response(200, 'Success')
    @data_ns.response(400, 'Bad Request')
    @data_ns.response(404, 'Not Found')
    @data_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @data_ns.doc(security="jsonWebToken")
    def put(self, data_id):
        """
        Updates data details by ID.
        """
        try:
            if not request.json or any(value == "" for value in request.json.values()):
                return {'message': 'Request body cannot be empty or contain empty values'}, 400

            data_details = DataUpdationDto(**request.json)           
            data = get_data_service(data_id)           
            if not data:
                return {'message': 'Data not found'}, 404

            update_data_service(data_id, data_details)
            return {'message': 'Data updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

@data_ns.route('/student/<string:student_id>')
class DataByStudent(Resource):
    @data_ns.response(200, 'Success')
    @data_ns.response(404, 'Not Found')
    @data_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @data_ns.doc(security="jsonWebToken")
    def get(self, student_id):
        """
        Gets data details by student ID.
        """
        try:
            data = get_data_by_student_id_service(student_id)
            if data:
                return data.__dict__, 200
            else:
                return {'message': 'Data not found for the specified student'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
