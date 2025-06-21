import uuid
from datetime import datetime


class BaseModel:
    """
    Base class for all models.
    """

    def __init__(self):
        """
        Initialize the object.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Save the object.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update the object.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
