from app.models.base import BaseModel
from app.models.user import User


class Place(BaseModel):
    """
    Class representing a place.
    """

    def __init__(
            self,
            title,
            description,
            price,
            latitude,
            longitude,
            owner,
            amenities=[]
            ):
        """
        Initialize a place.
        """
        super().__init__()

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = amenities

    @property
    def title(self):
        """
        Get the place title.
        """
        return self.__title

    @title.setter
    def title(self, value):
        """
        Set the place title.
        """
        if not isinstance(value, str) or len(value) > 100:
            raise ValueError(
                'Title must a maximum length of 100 characters'
            )
        self.__title = value

    @property
    def description(self):
        """
        Get the place description.
        """
        return self.__description

    @description.setter
    def description(self, value):
        """
        Set the place description.
        """
        if value is not None and not isinstance(value, str) or len(value) > 2048:
            raise ValueError(
                'Description must be a string with a maximum length of 2048 characters'
            )
        self.__description = value

    @property
    def price(self):
        """
        Get the place price.
        """
        return self.__price

    @price.setter
    def price(self, value):
        """
        Set the place price.
        """
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(
                'Price must be a positive number'
            )
        self.__price = value

    @property
    def latitude(self):
        """
        Get the place latitude.
        """
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        """
        Set the place latitude.
        """
        if not isinstance(value, (int, float)) or not (-90.0 <= value <= 90.0):
            raise ValueError(
                'Latitude must be a number between -90.0 and 90.0'
            )
        self.__latitude = value

    @property
    def longitude(self):
        """
        Get the place longitude.
        """
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        """
        Set the place longitude.
        """
        if not isinstance(value, (int, float)) or not (-180.0 <= value <= 180.0):
            raise ValueError(
                'Longitude must be a number between -180.0 and 180.0'
            )
        self.__longitude = value

    @property
    def owner(self):
        """
        Get the place owner.
        """
        return self.__owner

    @owner.setter
    def owner(self, value):
        """
        Set the place owner.
        """
        if not isinstance(value, User):
            raise ValueError(
                'Owner must be a User object'
                )
        self.__owner = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def remove_review(self, review):
        """Remove a review from the place."""
        self.reviews.remove(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
