from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """
    User Model
    Represents a user in the TaskFlow system.
    """

    def __init__(
        self,
        id=None,
        full_name="",
        email="",
        password="",
        role="Member",
        created_at=None
    ):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at

    # ----------------------------
    # Password Methods
    # ----------------------------

    def set_password(self, password):
        """Hash and store the password."""
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """Verify entered password."""
        return check_password_hash(self.password, password)

    # ----------------------------
    # Convert to Dictionary
    # ----------------------------

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at
        }

    # ----------------------------
    # String Representation
    # ----------------------------

    def __str__(self):
        return f"User({self.id}, {self.full_name}, {self.email}, {self.role})"