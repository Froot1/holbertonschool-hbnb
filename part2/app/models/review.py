from app.models.base import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    """
    Class representing a review of a place.
    """

    def __init__(
            self,
            text,
            rating,
            place,
            user):
        """
        Initialize a review.
        """
        super().__init__()

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        """
        Get the review text.
        """
        return self.__text

    @text.setter
    def text(self, value):
        """
        Set the review text.
        """
        if len(value) > 2048:
            raise ValueError('Text length exceeds 2048 characters')
        self.__text = value

    @property
    def rating(self):
        """
        Get the review rating.
        """
        return self.__rating

    @rating.setter
    def rating(self, value):
        """
        Set the review rating.
        """
        if value < 1 or value > 5:
            raise ValueError('Rating must be between 1 and 5')
        self.__rating = value

    @property
    def place(self):
        """
        Get the place.
        """
        return self.__place

    @place.setter
    def place(self, value):
        """
        Set the place.
        """
        if not value or not isinstance(value, Place):
            raise ValueError('Place must be provided')
        self.__place = value

    @property
    def user(self):
        """
        Get the user.
        """
        return self.__user

    @user.setter
    def user(self, value):
        """
        Set the user.
        """
        if not value or not isinstance(value, User):
            raise ValueError('User must be provided')
        self.__user = value
