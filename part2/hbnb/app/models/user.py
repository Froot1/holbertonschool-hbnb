from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        if not first_name or not last_name:
            raise ValueError("First name and last name are required")
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError("Names must be under 50 characters")

        if not email or "@" not in email:
            raise ValueError("A valid email is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
