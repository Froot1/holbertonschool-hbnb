import re

from app.models.base import BaseModel


class User(BaseModel):
    """
    Class representing a user of the application.
    """

    def __init__(
            self,
            first_name,
            last_name,
            email,
            is_admin=False):
        """
        Initialize a user.
        """
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        """
        Get the user's first name.
        """
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        """
        Set the user's first name.
        """
        if not value or len(value) > 50 or len(value) < 1:
            raise ValueError(
                'First name must be provided and be less than 50 characters'
                )
        self.__first_name = value

    @property
    def last_name(self):
        """
        Get the user's last name.
        """
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        """
        Set the user's last name.
        """
        if not value or len(value) > 50 or len(value) < 1:
            raise ValueError(
                'Last name must be provided and be less than 50 characters'
                )
        self.__last_name = value

    @property
    def email(self):
        """
        Get the user's email.
        """
        return self.__email

    @email.setter
    def email(self, value):
        """
        Set the user's email.
        """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise ValueError('Invalid email format')
        self.__email = value

    @property
    def is_admin(self):
        """
        Get the user's admin status.
        """
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        """
        Set the user's admin status.
        """
        if not isinstance(value, bool):
            raise ValueError('is_admin must be a boolean')
        self.__is_admin = value
