from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def test_user_creation():
    user = User(first_name="Fahad", last_name="Alonazi", email="Fahad@example.com")
    assert user.first_name == "Fahad"
    assert user.last_name == "Alonazi"
    assert user.email == "Fahad@example.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!") 


def test_place_creation():
    owner = User(first_name="Fahad", last_name="Alonazi", email="Fahad@example.com")
    place = Place(title="Our Apartment", description="A nice place to stay", price=500, latitude=50.123, longitude=-120.123, owner=owner)

    # Adding a review
    review = Review(text="Great stay!", rating=5, place_id=place.id, user_id=owner.id)
    place.add_review(review)

    assert place.title == "Our Apartment"
    assert place.price == 500
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Place creation and relationship test passed!")


def test_review_creation():
    owner = User(first_name="Fahad", last_name="Alonazi", email="Fahad@example.com")
    place = Place(title="Our Apartment", description="A nice place to stay", price=500, latitude=50.123, longitude=-120.123, owner=owner)
    review = Review(text="Great stay!", rating=5, place_id=place.id, user_id=owner.id)
    assert review.text == "Great stay!"
    assert review.rating == 5
    assert review.place_id == place.id
    assert review.user_id == owner.id
    print("Review creation test passed!")


def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")


if __name__ == "__main__":
    test_user_creation()
    test_place_creation()
    test_review_creation()
    test_amenity_creation()
