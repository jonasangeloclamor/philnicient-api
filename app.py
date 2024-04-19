from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from backend.controllers.user_controller import user_ns
from backend.controllers.class_controller import class_ns
from backend.controllers.student_controller import student_ns
from backend.controllers.model_result_controller import model_result_ns
from backend.controllers.assessment_result_controller import assessment_result_ns
from backend.controllers.assessment_controller import assessment_ns
from backend.controllers.question_controller import question_ns
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS", "security_config.DevelopmentConfig")
app.config.from_object(env_config)

# Enable CORS for the entire Flask app with specific origins
CORS(app, origins=['http://localhost:3000', 'https://philnicient.vercel.app'], supports_credentials=True)

# Initialize JWT manager
jwt = JWTManager(app)

# Initialize API with Swagger UI
api = Api(app, version='1.0', title='Philnicient API', description="A RESTful API for assessing BSCS students' proficiency in PhilNITS FE exam categories.")

# Add namespaces to API
api.add_namespace(user_ns)
api.add_namespace(class_ns)
api.add_namespace(student_ns)
api.add_namespace(model_result_ns)
api.add_namespace(assessment_result_ns)
api.add_namespace(assessment_ns)
api.add_namespace(question_ns)

if __name__ == '__main__':
    app.run(debug=True)
