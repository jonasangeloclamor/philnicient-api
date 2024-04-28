from flask import request
from flask_restx import Namespace, Resource, fields
from backend.services.user_service import create_user_service, get_user_service, get_all_users_service, get_user_by_username_service, get_user_by_email_service, login_user, update_user_password_service, delete_teacher_and_related_data_service, delete_student_and_related_data_service
from backend.data_components.dtos import UserCreationDto, UserLoginDto, ForgotPasswordRequestDto, ForgotPasswordResetDto
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, get_jti
from backend.utils.mail_util import generate_verification_code, send_verification_code, verification_codes
from security_config import authorizations
from backend.utils.auth import role_required
from backend.utils.blacklist import BLACKLIST

user_ns = Namespace('User', path='/api/users', description='Operations related to Users', authorizations=authorizations)

user_model = user_ns.model('UserCreationDto', {
    'firstname': fields.String(required=True, description='First Name'),
    'middlename': fields.String(required=True, description='Middle Name'),
    'lastname': fields.String(required=True, description='Last Name'),
    'email': fields.String(required=True, description='Email Address'),
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'role': fields.String(required=True, description='Role (Teacher or Student)')
})

user_login_model = user_ns.model('UserLoginDto', {
    'username_or_email': fields.String(required=True, description='Username or Email Address of the User'),
    'password': fields.String(required=True, description='Password of the User')
})

forgot_password_request_model = user_ns.model('ForgotPasswordRequestDto', {
    'email': fields.String(required=True, description='Email Address')
})

forgot_password_reset_model = user_ns.model('ForgotPasswordResetDto', {
    'email': fields.String(required=True, description='Email Address'),
    'code': fields.String(required=True, description='Verification Code'),
    'password': fields.String(required=True, description='New Password')
})

@user_ns.route('/login')
class UserLogin(Resource):
    @user_ns.expect(user_login_model)
    @user_ns.response(200, 'Success')
    @user_ns.response(400, 'Bad Request')
    @user_ns.response(401, 'Unauthorized')
    @user_ns.response(500, 'Internal Server Error')
    def post(self):
        """
        Logs in a user and returns user ID, role, access token, and refresh token.
        """
        try:
            user_login_data = UserLoginDto(**request.json)

            if not user_login_data.username_or_email or not user_login_data.password:
                return {'message': 'Username/email and password are required'}, 400

            user = login_user(user_login_data)
            if user:
                access_token = create_access_token(identity=user.id, expires_delta=False)
                refresh_token = create_refresh_token(identity=user.id, expires_delta=False)
                return {
                    'user_id': user.id,
                    'role': user.role,
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200
            else:
                return {'message': 'Invalid username, email, or password'}, 401
        except Exception as e:
            return {'message': str(e)}, 500

@user_ns.route('/logout')
class UserLogout(Resource):
    @jwt_required()
    @user_ns.doc(security="jsonWebToken")
    @user_ns.response(200, 'Success')
    @user_ns.response(500, 'Internal Server Error')
    def post(self):
        """
        Logs out a user by blacklisting the JWT token.
        """
        try:
            jti = get_jwt()['jti']
            BLACKLIST.add(jti)
            return {'message': 'Successfully logged out'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

@user_ns.route('/token/refresh')
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    @user_ns.doc(security="jsonWebToken")
    def post(self):
        """
        Refreshes an access token using the refresh token.
        """
        try:
            current_user = get_jwt_identity()
            new_access_token = create_access_token(identity=current_user, expires_delta=False)
            return {'access_token': new_access_token}, 200
        except Exception as e:
            return {'message': str(e)}, 500

@user_ns.route('')
class UserList(Resource):
    @user_ns.expect(user_model)
    @user_ns.response(201, 'Created')
    @user_ns.response(400, 'Bad Request')
    @user_ns.response(409, 'Conflict')
    @user_ns.response(500, 'Internal Server Error')
    def post(self):
        """
        Creates a new user.
        """
        try:
            user_data = UserCreationDto(**request.json)

            if user_data.role not in ['Teacher', 'Student']:
                return {'message': "Role must be either 'Teacher' or 'Student'"}, 400

            existing_user = get_user_by_username_service(user_data.username)
            if existing_user:
                return {'message': 'User with the same username already exists'}, 409
            
            existing_user_by_email = get_user_by_email_service(user_data.email)
            if existing_user_by_email:
                return {'message': 'User with the same email address already exists'}, 409
            
            user = create_user_service(user_data)
            return user.__dict__, 201
        except Exception as e:
            return {'message': str(e)}, 500

    @user_ns.response(200, 'Success')
    @user_ns.response(204, 'No Content')
    @user_ns.response(500, 'Internal Server Error')
    @role_required('Admin')
    @user_ns.doc(security="jsonWebToken")     
    def get(self):
        """
        Gets all users.
        """
        try:
            users = get_all_users_service()
            if users:
                return [user.__dict__ for user in users], 200
            else:
                return {'message': 'No users found'}, 204
        except Exception as e:
            return {'message': str(e)}, 500

@user_ns.route('/<string:user_id>')
class User(Resource):
    @user_ns.response(200, 'Success')
    @user_ns.response(404, 'Not Found')
    @user_ns.response(500, 'Internal Server Error')
    @role_required('Admin', 'Teacher')
    @user_ns.doc(security="jsonWebToken") 
    def get(self, user_id):
        """
        Gets user details by ID.
        """
        try:
            user = get_user_service(user_id)
            if user:
                return user.__dict__, 200
            else:
                return {'message': 'User not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

@user_ns.route('/<string:user_id>/delete-teacher')
class DeleteTeacher(Resource):
    @user_ns.response(200, 'Success')
    @user_ns.response(404, 'Not Found')
    @user_ns.response(500, 'Internal Server Error')
    @role_required('Admin')
    @user_ns.doc(security="jsonWebToken") 
    def delete(self, user_id):
        """
        Deletes teacher's details and related data by ID.
        """
        try:
            user = get_user_service(user_id)
            if user and user.role == "Teacher":
                delete_teacher_and_related_data_service(user_id)
                return {'message': 'Teacher deleted successfully'}, 200
            else:
                return {'message': 'Teacher not found'}, 404
        except ValueError as e:
            return {'message': str(e)}, 404
        except Exception as e:
            return {'message': str(e)}, 500

@user_ns.route('/<string:user_id>/delete-student')
class DeleteStudent(Resource):
    @user_ns.response(200, 'Success')
    @user_ns.response(404, 'Not Found')
    @user_ns.response(500, 'Internal Server Error')
    @role_required('Admin')
    @user_ns.doc(security="jsonWebToken") 
    def delete(self, user_id):
        """
        Deletes student's details and related data by ID.
        """
        try:
            user = get_user_service(user_id)
            if user and user.role == "Student":
                delete_student_and_related_data_service(user_id)
                return {'message': 'Student deleted successfully'}, 200
            else:
                return {'message': 'Student not found'}, 404
        except ValueError as e:
            return {'message': str(e)}, 404
        except Exception as e:
            return {'message': str(e)}, 500
        
@user_ns.route('/forgot-password')
class ForgotPassword(Resource):
    @user_ns.expect(forgot_password_request_model)
    @user_ns.response(200, 'Success')
    @user_ns.response(400, 'Bad Request')
    @user_ns.response(404, 'Not Found')
    @user_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Student')
    @user_ns.doc(security="jsonWebToken") 
    def post(self):
        """
        Sends a verification code to the provided email address for resetting the password.
        """
        try:
            email_data = ForgotPasswordRequestDto(**request.json)

            if not email_data.email:
                return {'message': 'Email address is required'}, 400

            user = get_user_by_email_service(email_data.email)
            if not user:
                return {'message': 'User not found'}, 404

            code = generate_verification_code()
            send_verification_code(email_data.email, code)
            
            return {'message': 'Verification code sent successfully to your email address'}, 200
        except Exception as e:
            return {'message': str(e)}, 500
        
@user_ns.route('/reset-password')
class ResetPassword(Resource):
    @user_ns.expect(forgot_password_reset_model)
    @user_ns.response(200, 'Success')
    @user_ns.response(400, 'Bad Request')
    @user_ns.response(500, 'Internal Server Error')
    @role_required('Teacher', 'Student')
    @user_ns.doc(security="jsonWebToken") 
    def post(self):
        """
        Resets the password using the verification code sent to the email address.
        """
        try:
            reset_data = ForgotPasswordResetDto(**request.json)

            if not reset_data.email or not reset_data.code or not reset_data.password:
                return {'message': 'Email address, verification code, and new password are required'}, 400
            
            if reset_data.email not in verification_codes:
                return {'message': 'Invalid email address or code'}, 400

            if verification_codes[reset_data.email] != reset_data.code:
                return {'message': 'Invalid or expired verification code'}, 400

            update_user_password_service(reset_data.email, reset_data.password)
            
            del verification_codes[reset_data.email]
            
            return {'message': 'Password reset successful'}, 200
        except Exception as e:
            return {'message': str(e)}, 500
        