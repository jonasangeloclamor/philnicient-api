from backend.repositories.user_repository import create_user, get_user, get_all_users, get_user_by_username, get_user_by_email, get_user_by_username_or_email, update_user_password
from backend.data_components.dtos import UserCreationDto, UserLoginDto
from backend.data_components.mappings import map_user_creation_dto_to_model
import bcrypt
import re

def create_user_service(user_data: UserCreationDto):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user_data.email):
        raise ValueError("Invalid email format")

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

def get_user_by_username_or_email_service(username_or_email):
    return get_user_by_username_or_email(username_or_email)

def get_user_by_email_service(email):
    return get_user_by_email(email)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def login_user(user_login_data: UserLoginDto):
    user = get_user_by_username_or_email(user_login_data.username_or_email)
    if user:
        if bcrypt.checkpw(user_login_data.password.encode('utf-8'), user.password.encode('utf-8')):
            return user
    return None

def update_user_password_service(email, new_password):
    user = get_user_by_email_service(email)
    if user:
        hashed_password = hash_password(new_password)
        user.password = hashed_password
        update_user_password(user.id, hashed_password)
    else:
        return None
