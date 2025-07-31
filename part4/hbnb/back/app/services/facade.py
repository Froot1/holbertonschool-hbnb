from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import UserRepository
from app.persistence.repository import PlaceRepository
from app.persistence.repository import ReviewRepository
from app.persistence.repository import AmenityRepository


class HBnBFacade:
    def __init__(self):
        """
        Initialize repositories.
        """
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    """
    User methods
    """
    def create_user(self, user_data):
        """
        Create a new user.
        """
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Get a user by ID.
        """
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """
        Get all users.
        """
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """
        Get a user by email.
        """
        return self.user_repo.get_by_email(email)

    def update_user(self, user_id, user_data):
        """
        Update a user.
        """
        self.user_repo.update(user_id, **user_data)

    def delete_user(self, user_id):
        """
        Delete a user.
        """
        self.user_repo.delete(user_id)

    """
    Amenity methods
    """
    def create_amenity(self, amenity_data):
        """
        Create a new amenity.
        """
        new_amenity = Amenity(**amenity_data)
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        """
        Get an amenity by ID.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Get all amenities.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an amenity.
        """
        return self.amenity_repo.update(amenity_id, **amenity_data)

    def delete_amenity(self, amenity_id):
        """
        Delete an amenity.
        """
        return self.amenity_repo.delete(amenity_id)

    """
    Place methods
    """
    def create_place(self, place_data):
        """
        Create a new place.
        """
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Get a place by ID.
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Get all places.
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Update a place.
        """
        self.place_repo.update(place_id, **place_data)

    def delete_place(self, place_id):
        """
        Delete a place.
        """
        self.place_repo.delete(place_id)

    """
    Review methods
    """
    def create_review(self, review_data):
        """
        Create a new review.
        """
        new_review = Review(**review_data)
        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        """
        Get a review by ID.
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Get all reviews.
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Get all reviews for a place.
        """
        return self.review_repo.get_reviews_by_place(place_id)

    def update_review(self, review_id, review_data):
        """
        Update a review.
        """
        return self.review_repo.update(review_id, **review_data)

    def delete_review(self, review_id):
        """
        Delete a review.
        """
        return self.review_repo.delete(review_id)
