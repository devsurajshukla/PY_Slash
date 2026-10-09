from db import get_db_connection
import re


def is_valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.fullmatch(pattern, email) is not None


def get_users():
    db = None
    cursor = None

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        return users

    except Exception as e:
        print(f"Error fetching users: {e}")
        raise

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


def create_user(user_data):

    if not user_data:
        return None, "Request body is required."

    required_fields = ["name", "email", "role"]

    for field in required_fields:
        if field not in user_data:
            return None, f"{field} is required."

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

        # Check duplicate email
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )

        dup = cursor.fetchone()

        if dup:
            return None, "Email already exists."

        # Insert user
        query = """
            INSERT INTO users (name, email, role)
            VALUES (%s, %s, %s)
        """

        value = (name, email, role)

        cursor.execute(query, value)
        db.commit()

        new_user_id = cursor.lastrowid

        new_user = {
            "id": new_user_id,
            "name": name,
            "email": email,
            "role": role
        }

        return new_user, None

    except Exception as e:

        if db:
            db.rollback()

        print(f"Error creating user: {e}")
        raise

    finally:

        if cursor:
            cursor.close()

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