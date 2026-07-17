from models.user import User
from database.db import Database


class AuthService:

    def __init__(self):
        self.db = Database()
        self.db.connect()

    # ==========================================
    # Register User
    # ==========================================

    def register(self, full_name, email, password):

        # Check existing email
        query = """
            SELECT id
            FROM users
            WHERE email=%s
        """

        existing = self.db.fetchone(query, (email,))

        if existing:
            return {
                "success": False,
                "message": "Email already exists."
            }

        # Create User object
        user = User(
            full_name=full_name,
            email=email
        )

        user.set_password(password)

        insert_query = """
            INSERT INTO users
            (
                full_name,
                email,
                password,
                role
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
        """

        self.db.execute(
            insert_query,
            (
                user.full_name,
                user.email,
                user.password,
                user.role
            )
        )

        return {
            "success": True,
            "message": "Registration Successful."
        }

    # ==========================================
    # Login
    # ==========================================

    def login(self, email, password):

        query = """
            SELECT *
            FROM users
            WHERE email=%s
        """

        data = self.db.fetchone(query, (email,))

        if not data:
            return None

        user = User(
            id=data["id"],
            full_name=data["full_name"],
            email=data["email"],
            password=data["password"],
            role=data["role"],
            created_at=data["created_at"]
        )

        if user.verify_password(password):
            return user

        return None

    # ==========================================
    # Get User By ID
    # ==========================================

    def get_user(self, user_id):

        query = """
            SELECT *
            FROM users
            WHERE id=%s
        """

        data = self.db.fetchone(query, (user_id,))

        if not data:
            return None

        return User(
            id=data["id"],
            full_name=data["full_name"],
            email=data["email"],
            password=data["password"],
            role=data["role"],
            created_at=data["created_at"]
        )

    # ==========================================
    # Delete User
    # ==========================================

    def delete_user(self, user_id):

        query = """
            DELETE
            FROM users
            WHERE id=%s
        """

        self.db.execute(query, (user_id,))

    # ==========================================
    # Get All Users
    # ==========================================

    def get_all_users(self):

        query = """
            SELECT *
            FROM users
            ORDER BY id
        """

        return self.db.fetchall(query)