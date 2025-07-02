from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.models.base import BaseModel


place_amenity = db.Table(
    'place_amenity',
    db.Column(
        'place_id',
        db.String(36),
        db.ForeignKey('places.id'),
        primary_key=True
    ),
    db.Column(
        'amenity_id',
        db.String(36),
        db.ForeignKey('amenities.id'),
        primary_key=True
    )
)


class Place(BaseModel):
    """
    Class representing a place.
    """

    __tablename__ = 'places'

    _title = db.Column(db.String(255), nullable=False)
    _description = db.Column(db.Text, nullable=True)
    _price = db.Column(db.Numeric(10, 2), nullable=False)
    _latitude = db.Column(db.Float, nullable=False)
    _longitude = db.Column(db.Float, nullable=False)
    _owner_id = db.Column(db.String(36),
                          db.ForeignKey('users.id'),
                          nullable=False)
    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review',
                              back_populates='place',
                              cascade='all, delete-orphan')
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        back_populates='places',
        cascade='all, delete'
    )

    @hybrid_property
    def title(self):
        """
        Get the place title.
        """
        return self._title

    @title.setter
    def title(self, value):
        """
        Set the place title.
        """
        if not isinstance(value, str) or len(value) > 255:
            raise ValueError(
                'Title must a maximum length of 255 characters.'
            )
        self._title = value

    @hybrid_property
    def description(self):
        """
        Get the place description.
        """
        return self._description

    @description.setter
    def description(self, value):
        """
        Set the place description.
        """
        if value and not isinstance(value, str) or len(value) > 2048:
            raise ValueError(
                'Description must be a string with a\
                 maximum length of 2048 characters.'
            )
        self._description = value

    @hybrid_property
    def price(self):
        """
        Get the place price.
        """
        return self._price

    @price.setter
    def price(self, value):
        """
        Set the place price.
        """
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(
                'Price must be a positive number.'
            )
        self._price = value

    @hybrid_property
    def latitude(self):
        """
        Get the place latitude.
        """
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """
        Set the place latitude.
        """
        if not isinstance(value, (int, float)) or not (-90.0 <= value <= 90.0):
            raise ValueError(
                'Latitude must be a number between -90.0 and 90.0.'
            )
        self._latitude = value

    @hybrid_property
    def longitude(self):
        """
        Get the place longitude.
        """
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """
        Set the place longitude.
        """
        if not isinstance(value, (int, float)):
            raise ValueError(
                'Longitude must be a number between -180.0 and 180.0.'
            )
        elif not (-180.0 <= value <= 180.0):
            raise ValueError(
                'Longitude must be a number between -180.0 and 180.0.'
            )
        self._longitude = value

    @hybrid_property
    def owner_id(self):
        """
        Get the place owner's ID.
        """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        """
        Set the place owner's ID.
        """
        if not isinstance(value, str) or len(value) != 36:
            raise ValueError(
                'Owner ID must be a string of 36 characters.'
            )
        self._owner_id = value
