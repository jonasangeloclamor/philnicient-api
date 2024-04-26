from flask import Flask, jsonify
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
from backend.utils.blacklist import BLACKLIST
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS", "security_config.DevelopmentConfig")
app.config.from_object(env_config)
CORS(app, supports_credentials=True)

# Initialize JWT manager
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLACKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"message": "The token has been revoked."}
        ),
        401,
    )

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
