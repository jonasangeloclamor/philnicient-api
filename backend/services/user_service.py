from backend.repositories.user_repository import create_user, get_user, get_all_users, get_user_by_username
from backend.data_components.dtos import UserCreationDto, UserLoginDto
from backend.data_components.mappings import map_user_creation_dto_to_model
import bcrypt

def create_user_service(user_data: UserCreationDto):
    user = map_user_creation_dto_to_model(user_data)
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    user_id = create_user(user)
    user.id = user_id
    return user

def get_user_service(user_id):
    return get_user(user_id)

def get_all_users_service():
    return get_all_users()

def get_user_by_username_service(username):
    return get_user_by_username(username)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def login_user(username, password: UserLoginDto):
    user = get_user_by_username(username)
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
    return None
