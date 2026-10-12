from db import get_db_connection
from db_sqlalchemy import get_db_session
from sqlalchemy.exc import IntegrityError
from models.user import User
import bcrypt
import re



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


def get_users():
    db = None

    try:
        db = get_db_session()
        users = db.query(User).all()

        users_data = []

        for user in users:
            users_data.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            })

        return users_data

    except Exception as e:
        print(f"Error fetching users: {e}")
        raise

    finally:
        if db:
            db.close()


def create_user(user_data):
    db = None

    try:

        if not user_data:
            return None, "Request body is required."

        required_fields = ["name", "email", "password", "role"]

        for field in required_fields:
            if field not in user_data:
                return None, f"{field} is required."

        name = user_data["name"].strip()
        email = user_data["email"].strip()
        password = user_data["password"]
        role = user_data["role"].strip()

        # Empty value validation
        if not name:
            return None, "Name cannot be empty."

        if not email:
            return None, "Email cannot be empty."

        if not password:
            return None, "Password cannot be empty."
        
        if len(password) < 8:
                return None, "Password must be at least 8 characters"

        if not role:
            return None, "Role cannot be empty."

        # Email validation
        if not is_valid_email(email):
            return None, "Invalid email address."

        db = get_db_session()

        existing_user = db.query(User).filter_by(email=email).first()

        if existing_user:
            return None, "Email already exists."

        hashed_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

        new_user = User(
                name=name,
                email=email,
                role=role,
                password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "role": new_user.role
            }, None

    except Exception as e:
        if db:
         db.rollback()

        print(f"Error creating user: {e}")
        raise

    finally:
        if db:
            db.close()




def update_user(user_id, user_data):

    if not user_data:
        return None, "Request body is required."

    required_fields = ["name", "email", "role"]

    for field in required_fields:
        if field not in user_data:
            return None, f"{field} is required."

    # Get values OUTSIDE the for loop
    name = user_data["name"].strip()
    email = user_data["email"].strip()
    role = user_data["role"].strip()

    # Empty value validation
    if not name:
        return None, "Name cannot be empty."

    if not email:
        return None, "Email cannot be empty."

    if not role:
        return None, "Role cannot be empty."

    # Email validation
    if not is_valid_email(email):
        return None, "Invalid email address."

    db = None
    cursor = None

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Check if user exists
        cursor.execute(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            return None, "User not found."

        # Check duplicate email
        # Exclude current user's own ID
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            AND id != %s
            """,
            (email, user_id)
        )

        dup = cursor.fetchone()

        if dup:
            return None, "Email already exists."

        # Update user
        query = """
            UPDATE users
            SET name = %s,
                email = %s,
                role = %s
            WHERE id = %s
        """

        value = (name, email, role, user_id)

        cursor.execute(query, value)
        db.commit()

        # Get updated user
        cursor.execute(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )

        updated_user = cursor.fetchone()

        return updated_user, None

    except Exception as e:

        if db:
            db.rollback()

        print(f"Error updating user: {e}")
        raise

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()


def delete_user(user_id):

    db = None
    cursor = None

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Check if user exists
        cursor.execute(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            return False, "User not found."

        # Delete user
        cursor.execute(
            "DELETE FROM users WHERE id = %s",
            (user_id,)
        )

        db.commit()

        return True, None

    except Exception as e:

        if db:
            db.rollback()

        print(f"Error deleting user: {e}")
        raise

    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()