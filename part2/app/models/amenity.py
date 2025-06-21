from app.models.base import BaseModel


class Amenity(BaseModel):
    """
    Class representing an amenity.
    """

    def __init__(self, name):
        """
        Initialize an amenity.
        """
        super().__init__()

        self.name = name

    @property
    def name(self):
        """
        Get the amenity name.
        """
        return self.__name

    @name.setter
    def name(self, value):
        """
        Set the amenity name.
        """
        if not value or len(value) > 128:
            raise ValueError(
                'Name must be provided and be less than 128 characters'
                )
        self.__name = value
