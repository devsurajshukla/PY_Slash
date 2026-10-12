from db_sqlalchemy import get_db_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from models.user import User
import bcrypt
import re
import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()



def is_valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.fullmatch(pattern, email) is not None

def user_to_dict(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }

def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

def generate_token(user):
    secret_key = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY is not configured.")

    payload = {
        "sub": str(user.id),
        "role": user.role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        secret_key,
        algorithm="HS256"
    )

    return token


def get_users():
    with get_db_session() as db:
        users = db.scalars(select(User)).all()
        return [user_to_dict(user) for user in users]

def create_user(user_data):
    if not user_data:
        return None, "Request body is required."
    
    required_fields = ["name", "email", "password", "role"]
    for field in required_fields:
        if field not in user_data:
            return None, f"{field} is required."

    name = user_data["name"]
    email = user_data["email"]
    password = user_data["password"]
    role = user_data["role"]

    if not all(isinstance(v, str) for v in
               [name, email, password, role]):
        return None, "All fields must be strings."

    name = name.strip()
    email = email.strip()
    role = role.strip()

    if not name:
        return None, "Name cannot be empty."

    if not email:
        return None, "Email cannot be empty."

    if not password:
        return None, "Password cannot be empty."

    if len(password) < 8:
        return None, "Password must be at least 8 characters."

    if not role:
        return None, "Role cannot be empty."

    if not is_valid_email(email):
        return None, "Invalid email address."

    # bcrypt has a 72-byte password limit.
    if len(password.encode("utf-8")) > 72:
        return None, "Password must not exceed 72 UTF-8 bytes."

    with get_db_session() as db:
        try:
            existing = db.scalar(
                select(User).where(User.email == email)
            )

            if existing:
                return None, "Email already exists."

            new_user = User(
                name=name,
                email=email,
                role=role,
                password=hash_password(password)
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return user_to_dict(new_user), None

        except IntegrityError:
            db.rollback()
            return None, "Email already exists or data is invalid."

        except Exception:
            db.rollback()
            raise




def update_user(user_id, user_data):

    if not user_data:
        return None, "Request body is required."

    required_fields = ["name", "email", "role"]
    for field in required_fields:
        if field not in user_data:
            return None, f"{field} is required."
        
    name = user_data["name"].strip()
    email = user_data["email"].strip()
    role = user_data["role"].strip()

    if not all(isinstance(v, str) for v in [name, email, role]):
        return None, "Name, email and role must be strings."

    name = name.strip()
    email = email.strip()
    role = role.strip()

    # Empty value validation
    if not name:
        return None, "Name cannot be empty."

    if not email:
        return None, "Email cannot be empty."

    if not role:
        return None, "Role cannot be empty."
    
    if not is_valid_email(email):
            return None, "Invalid email address."

    password = user_data.get("password")

    if password is not None:
        if not isinstance(password, str):
            return None, "Password must be a string."

        if not password:
            return None, "Password cannot be empty."

        if len(password) < 8:
            return None, "Password must be at least 8 characters."

        if len(password.encode("utf-8")) > 72:
            return None, "Password must not exceed 72 UTF-8 bytes."


    with get_db_session() as db:
        try:
            user = db.scalar(
                select(User).where(User.id == user_id)
            )

            if not user:
                return None, "User not found."

            # Check for email uniqueness
            existing_user = db.scalar(
                select(User).where(User.email == email, User.id != user_id)
            )

            if existing_user:
                return None, "Email already exists."

            user.name = name
            user.email = email
            user.role = role

            if password is not None:
                user.password = hash_password(password)

            db.commit()
            db.refresh(user)

            return user_to_dict(user), None

        except IntegrityError:
            db.rollback()
            return None, "Email already exists or data is invalid."

        except Exception:
            db.rollback()
            raise


def delete_user(user_id):
    with get_db_session() as db:
        try:
            user = db.get(User, user_id)

            if not user:
                return False, "User not found."

            db.delete(user)
            db.commit()

            return True, None

        except Exception:
            db.rollback()
            raise


def login_user(email, password):
    if not isinstance(email, str) or not email.strip():
        return None, "Email and password are required."

    if not isinstance(password, str) or not password:
        return None, "Email and password are required."

    with get_db_session() as db:
        user = db.scalar(
            select(User).where(User.email == email.strip())
        )

        if not user:
            return None, "Invalid email or password."

        try:
            password_valid = bcrypt.checkpw(
                password.encode("utf-8"),
                user.password.encode("utf-8")
            )
        except (ValueError, TypeError):
            password_valid = False

        if not password_valid:
            return None, "Invalid email or password."

        user_data = user_to_dict(user)
        token = generate_token(user)

        return {
            "token": token,
            "user": user_data
        }, None
