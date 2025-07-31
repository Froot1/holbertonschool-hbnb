from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.models.base import BaseModel


class Review(BaseModel):
    """
    Class representing a review of a place.
    """

    __tablename__ = 'reviews'

    _text = db.Column(db.Text, nullable=False)
    _rating = db.Column(db.Integer, nullable=False)
    _place_id = db.Column(db.String(36),
                          db.ForeignKey('places.id'),
                          nullable=False)
    _user_id = db.Column(db.String(36),
                         db.ForeignKey('users.id'),
                         nullable=False)
    user = db.relationship('User', back_populates='reviews')
    place = db.relationship('Place', back_populates='reviews')

    @hybrid_property
    def text(self):
        """
        Get the review text.
        """
        return self._text

    @text.setter
    def text(self, value):
        """
        Set the review text.
        """
        if len(value) > 2048:
            raise ValueError('Text length exceeds 2048 characters.')
        self._text = value

    @hybrid_property
    def rating(self):
        """
        Get the review rating.
        """
        return self._rating

    @rating.setter
    def rating(self, value):
        """
        Set the review rating.
        """
        if value < 1 or value > 5:
            raise ValueError('Rating must be between 1 and 5.')
        self._rating = value

    @hybrid_property
    def place_id(self):
        """
        Get the place.
        """
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        """
        Set the place.
        """
        if not isinstance(value, str) or len(value) != 36:
            raise ValueError(
                'Place ID must be a string of 36 characters.'
            )
        self._place_id = value

    @hybrid_property
    def user_id(self):
        """
        Get the user.
        """
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        """
        Set the user.
        """
        if not isinstance(value, str) or len(value) != 36:
            raise ValueError(
                'User ID must be a string of 36 characters.'
                )
        self._user_id = value
