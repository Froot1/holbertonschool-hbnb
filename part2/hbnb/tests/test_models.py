from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Test User
user = User("Alice", "Smith", "alice@example.com")
print("✅ User created:", user.first_name, user.last_name, user.email)

# Test Place
place = Place("Cozy Apartment", "Nice and quiet", 120, 45.0, 90.0, user)
print("✅ Place created:", place.title, "by", place.owner.first_name)

# Test Amenity
wifi = Amenity("Wi-Fi")
parking = Amenity("Parking")
place.add_amenity(wifi)
place.add_amenity(parking)
print("✅ Amenities added:", [a.name for a in place.amenities])

# Test Review
review = Review("Great stay!", 5, place, user)
place.add_review(review)
print("✅ Review added:", place.reviews[0].text)

