from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from backend.controllers.user_controller import user_ns
from backend.controllers.class_controller import class_ns
from backend.controllers.student_controller import student_ns
from backend.controllers.data_controller import data_ns

# Initialize Flask app
app = Flask(__name__)

# Initialize JWT manager
app.config['JWT_SECRET_KEY'] = 'philnits-api'
jwt = JWTManager(app)

# Initialize API with Swagger UI
api = Api(app, version='1.0', title='PhilNITS FE Proficiency API', description='Access a comprehensive suite of tools for management purposes with our API.')

# Add namespaces to API
api.add_namespace(user_ns)
api.add_namespace(class_ns)
api.add_namespace(student_ns)
api.add_namespace(data_ns)

if __name__ == '__main__':
    app.run(debug=True)
