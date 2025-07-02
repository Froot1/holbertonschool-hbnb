import re

from sqlalchemy.ext.hybrid import hybrid_property

from app import bcrypt, db
from app.models.base import BaseModel


class User(BaseModel):
    """
    Class representing a user of the application.
    """

    __tablename__ = 'users'

    _first_name = db.Column(db.String(255), nullable=False)
    _last_name = db.Column(db.String(255), nullable=False)
    _email = db.Column(db.String(255), nullable=False, unique=True)
    _password = db.Column(db.String(255), nullable=False)
    _is_admin = db.Column(db.Boolean, default=False)
    places = db.relationship('Place',
                             back_populates='owner',
                             cascade='all, delete-orphan')
    reviews = db.relationship('Review',
                              back_populates='user',
                              cascade='all, delete-orphan')

    @hybrid_property
    def first_name(self):
        """
        Get the user's first name.
        """
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """
        Set the user's first name.
        """
        if not value or len(value) > 255 or len(value) < 1:
            raise ValueError(
                'First name must be provided and be less than 255 characters.'
                )
        self._first_name = value

    @hybrid_property
    def last_name(self):
        """
        Get the user's last name.
        """
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """
        Set the user's last name.
        """
        if not value or len(value) > 255 or len(value) < 1:
            raise ValueError(
                'Last name must be provided and be less than 255 characters.'
                )
        self._last_name = value

    @hybrid_property
    def email(self):
        """
        Get the user's email.
        """
        return self._email

    @email.setter
    def email(self, value):
        """
        Set the user's email.
        """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not value or len(value) > 255:
            raise ValueError(
                'Email must be provided and be less than 255 characters.'
                )
        if not re.match(email_regex, value):
            raise ValueError('Invalid email format.')
        self._email = value

    @hybrid_property
    def is_admin(self):
        """
        Get the user's admin status.
        """
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        """
        Set the user's admin status.
        """
        if not isinstance(value, bool):
            raise ValueError('is_admin must be a boolean.')
        self._is_admin = value

    def hash_password(self, pwd):
        """Hashes the password before storing it."""
        self._password = bcrypt.generate_password_hash(pwd).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    @hybrid_property
    def password(self):
        """
        Get the user's password.
        """
        return self._password

    @password.setter
    def password(self, value):
        """
        Set the user's password.
        """
        if not value or len(value) < 8:
            raise ValueError('Password must be at least 8 characters.')
        if len(value) > 255:
            raise ValueError('Password must be less than 255 characters.')
        self.hash_password(value)
