import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from flask import request
from flask_restx import Namespace, Resource, fields
from backend.services.model_result_service import create_model_result_service, get_model_result_service, get_all_model_results_service, update_model_result_service, get_model_result_by_student_id_service
from backend.data_components.dtos import ModelResultCreationDto, ModelResultUpdationDto, ModelResultPredictionDto
from security_config import authorizations
from flask_jwt_extended import jwt_required

model_result_ns = Namespace('ModelResult', path='/api/model_results', description='Operations related to Model Results', authorizations=authorizations)

file_path = 'model/Categorized_Shuffled_Dataset.csv'
dataset = pd.read_csv(file_path)

knn_model = joblib.load('model/knnmodel.pkl')
scaler = joblib.load('model/scaler.pkl')

result_model = model_result_ns.model('ModelResultCreationDto', {
    'major_category': fields.String(required=True, description='Major Category'),
    'number_of_items': fields.Integer(required=True, description='Number of Items'),
    'total_score': fields.Integer(required=True, description='Total Score'),
    'total_time_taken': fields.Integer(required=True, description='Total Time Taken'),
    'average_cri': fields.Float(required=True, description='Average CRI'),
    'cri_criteria': fields.String(required=True, description='CRI Criteria'),
    'student_id': fields.String(required=True, description='Student ID')
})

update_result_model = model_result_ns.model('ModelResultUpdationDto', {
    'major_category': fields.String(required=True, description='Major Category'),
    'number_of_items': fields.Integer(required=True, description='Number of Items'),
    'total_score': fields.Integer(required=True, description='Total Score'),
    'total_time_taken': fields.Integer(required=True, description='Total Time Taken'),
    'average_cri': fields.Float(required=True, description='Average CRI'),
    'cri_criteria': fields.String(required=True, description='CRI Criteria'),
    'student_id': fields.String(required=True, description='Student ID')
})

result_prediction_model = model_result_ns.model('ModelResultPredictionDto', {
    'major_category': fields.Integer(required=True, description='Major Category'),
    'number_of_items': fields.Integer(required=True, description='Number of Items'),
    'total_score': fields.Integer(required=True, description='Total Score'),
    'total_time_taken': fields.Integer(required=True, description='Total Time Taken'),
    'average_cri': fields.Float(required=True, description='Average CRI')
})

@model_result_ns.route('/predict-cri-criteria')
class ModelResultPrediction(Resource):
    @model_result_ns.expect(result_prediction_model)
    @model_result_ns.response(200, 'Success')
    @model_result_ns.response(500, 'Internal Server Error')
    def post(self):
        """
        Predicts CRI criteria based on inputs.
        """
        try:
            prediction_inputs = ModelResultPredictionDto(**request.json)

            prediction_data = np.array([[prediction_inputs.major_category,
                                         prediction_inputs.number_of_items,
                                         prediction_inputs.total_score,
                                         prediction_inputs.total_time_taken,
                                         prediction_inputs.average_cri]])

            scaled_prediction_data = scaler.transform(prediction_data)
            predicted_cri_criteria = knn_model.predict(scaled_prediction_data)

            X_train = dataset.iloc[:, :-1].values
            y_train = dataset.iloc[:, -1].values

            X_train_scaled = scaler.transform(X_train)

            y_pred_train = knn_model.predict(X_train_scaled)

            accuracy = accuracy_score(y_train, y_pred_train)

            return {
                'predicted_cri_criteria': predicted_cri_criteria[0],
                'accuracy': accuracy
            }, 200

        except Exception as e:
            return {'message': str(e)}, 500

@model_result_ns.route('')
class ModelResultList(Resource):
    @model_result_ns.expect(result_model)
    @model_result_ns.response(201, 'Created')
    @model_result_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @model_result_ns.doc(security="jsonWebToken")
    def post(self):
        """
        Creates a new model result.
        """
        try:
            model_result_details = ModelResultCreationDto(**request.json)
            model_result = create_model_result_service(model_result_details)
            return model_result.__dict__, 201
        except Exception as e:
            return {'message': str(e)}, 500

    @model_result_ns.response(200, 'Success')
    @model_result_ns.response(204, 'No Content')
    @model_result_ns.response(500, 'Internal Server Error')    
    def get(self):
        """
        Gets all model results.
        """
        try:
            model_results = get_all_model_results_service()
            if model_results:
                return [rst.__dict__ for rst in model_results], 200
            else:
                return {'message': 'No model results found'}, 204
        except Exception as e:
            return {'message': str(e)}, 500

@model_result_ns.route('/<string:model_result_id>')
class ModelResult(Resource):
    @model_result_ns.response(200, 'Success')
    @model_result_ns.response(404, 'Not Found')
    @model_result_ns.response(500, 'Internal Server Error')
    def get(self, model_result_id):
        """
        Gets model result details by ID.
        """
        try:
            model_result = get_model_result_service(model_result_id)
            if model_result:
                return model_result.__dict__, 200
            else:
                return {'message': 'Model result not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

    @model_result_ns.expect(update_result_model)
    @model_result_ns.response(200, 'Success')
    @model_result_ns.response(400, 'Bad Request')
    @model_result_ns.response(404, 'Not Found')
    @model_result_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @model_result_ns.doc(security="jsonWebToken")
    def put(self, model_result_id):
        """
        Updates model result details by ID.
        """
        try:
            if not request.json or any(value == "" for value in request.json.values()):
                return {'message': 'Request body cannot be empty or contain empty values'}, 400

            model_result_details = ModelResultUpdationDto(**request.json)           
            model_result = get_model_result_service(model_result_id)           
            if not model_result:
                return {'message': 'Model result not found'}, 404

            update_model_result_service(model_result_id, model_result_details)
            return {'message': 'Model result updated successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

@model_result_ns.route('/students/<string:student_id>')
class ModelResultByStudent(Resource):
    @model_result_ns.response(200, 'Success')
    @model_result_ns.response(404, 'Not Found')
    @model_result_ns.response(500, 'Internal Server Error')
    @jwt_required()
    @model_result_ns.doc(security="jsonWebToken")
    def get(self, student_id):
        """
        Gets model result details by student ID.
        """
        try:
            model_result = get_model_result_by_student_id_service(student_id)
            if model_result:
                return model_result.__dict__, 200
            else:
                return {'message': 'Model result not found for the specified student'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
