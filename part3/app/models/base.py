import uuid
from datetime import datetime

from app import db


class BaseModel(db.Model):
    """
    Base class for all models.
    """

    __abstract__ = True

    id = db.Column(db.String(36),
                   primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

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
