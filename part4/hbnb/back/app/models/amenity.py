from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.models.base import BaseModel
from app.models.place import place_amenity


class Amenity(BaseModel):
    """
    Class representing an amenity.
    """

    __tablename__ = 'amenities'

    _name = db.Column(db.String(255), nullable=False)
    places = db.relationship('Place',
                             secondary=place_amenity,
                             back_populates='amenities')

    @hybrid_property
    def name(self):
        """
        Get the amenity name.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the amenity name.
        """
        if not value or len(value) > 255:
            raise ValueError(
                'Name must be provided and be less than 255 characters.'
                )
        self._name = value
