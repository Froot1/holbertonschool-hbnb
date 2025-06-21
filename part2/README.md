# HBNB - Part 2 - Implementation of Business Logic and API Endpoints

## Table of Contents
- [HBNB - Part 2](#hbnb---part-2)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Installation](#installation)
  - [Usage](#usage)
  - [File Structure](#file-structure)
  - [Explanation](#explanation)
	- [User](#user)
    - [Amenity](#amenity)
    - [Places](#places)
    - [Reviews](#reviews)
  - [Authors](#authors)

## Description
HBNB is a web application that allows users to manage and book places. This project is part of the Holberton School curriculum and focuses on implementing a full-stack web application.

## Installation
To install and run this project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Froot1/holbertonschool-hbnb
    ```
2. Navigate to the project directory:
    ```bash
    cd holbertonschool-hbnb/part2/hbnb
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To start the application, run the following command:
```bash
python3 run.py
```
Open your web browser and navigate to `http://localhost:5000/api/v1/` to access the application.

## File Structure
```
part2/hbnb/
├── api
│   ├── __init__.py
│   ├── v1
│   │   ├── __init__.py
│   │   ├── amenities.py
│   │   ├── places.py
│   │   ├── reviews.py
│   │   └── users.py
├── models
│   ├── __init__.py
│   ├── base.py
│   ├── amenity.py
│   ├── place.py
│   ├── review.py
│   └── user.py
├── persistence
│   ├── __init__.py
│   └── repository.py
├── services
│   ├── __init__.py
│   └── facade.py
├── config.py
├── requirements.txt
└── run.py
```

## Explanation

### User
A POST method is sent to register a new user. It retrieves the data from the API payload and create a new amenity using a **'facade.create_user'**. When a ValueError occurs, it returns an 400 status code error message. If successful, it returns the newly created user's ID and name with a 201 status code.
```python
def post(self):
        """Register a new user"""
        user_data = api.payload

        user = facade.get_user_by_email(user_data['email'])
        if user:
            return {'error': 'Email already registered'}, 400

        try:
            user = facade.create_user(user_data)
        except Exception as e:
            return {'error': str(e)}, 400
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            }, 200
```
**Expected input:**

```http
POST /api/v1/users/
accept: application/json
Content-Type: application/json

{
  "first_name": "Fahad",
  "last_name": "Alonazi",
  "email": "Fahad@example.com"
}
```

**Expected Response:**

```jsonc
{
  "id": "489aa957-5cc4-45bc-91c2-d016310f40d7",
  "first_name": "Fahad",
  "last_name": "Alonazi",
  "email": "Fahad@example.com"
}
// 201 User successfully created
```

### Amenity
A POST method is sent to register a new amenity. It retrieves the data from the API payload and create a new amenity using a **'facade.create_amenity'**. When a ValueError occurs, it returns an 400 status code error message. If successful, it returns the newly created aneminy's ID and name with a 201 status code.
```python
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        try:
            amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {
            'id': amenity.id,
            'name': amenity.name
            }, 201
```

**Expected input:**
```http
POST /api/v1/amenities/
Content-Type: application/json

{
  "name": "Swimming Pool"
}
```

**Expected Response:**

```jsonc
{
  "id": "0c25aedf-fda9-4dd8-a6f6-10c3012d6d32",
  "name": "Swimming Pool"
}

// 201 Amenity successfully created
```

**Possible Status Codes:**

- 201 Created: When the amenity is successfully created.
- 400 Bad Request: If input data is invalid.
---
### Places
The get method retrieves a list of all places by calling **'facade.get_all_places()'**. It initializes an empty list, iterates through the retrieved places, and appends each place's id, title, latitude, and longitude to the list. Finally, it returns this list with a status code of 200 to indicate success.
```python
    def get(self):
        """Retrieve a list of all places"""
        places = []
        for place in facade.get_all_places():
            places.append(
                {
                    'id': place.id,
                    'title': place.title,
                    'latitude': place.latitude,
                    'longitude': place.longitude
                }
                )
        return places, 200
```

**Expected input:**
```http
GET /api/v1/places/
Content-Type: application/json
```

**Expected Response:**

```jsonc
[
  {
    "id": "3ada9273-4498-4f7e-b189-ddedd22071f6",
    "title": "Our Apartment",
    "latitude": 50.123,
    "longitude": -120.123
  },
  ...
]

// 200 OK
```

**Possible Status Codes:**

- 200 OK: List of places retrieved successfully.

---
### Reviews
The put method updates an existing review based on the provided **'review_id'**. By checking the Review existence, it returns a 404 status code in case it doesn't exist. Check the input data if it's empty. If not, it updates the review using **'facade.update_review'** and returns a 200 status code if successful.
```python
    def put(self, review_id):
        """Update a review's information"""
        if facade.get_review(review_id) is None:
            return {'error': 'Review not found'}, 404

        review_data = api.payload
        if review_data == {}:
            return {'error': 'Invalid input data'}, 400
        try:
            facade.update_review(review_id, review_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {'message': 'Review updated successfully'}, 200
```

**Expected input:**
```http
PUT /api/v1/reviews/<review_id>
Content-Type: application/json

{
  "text": "Amazing Place!",
  "rating": 5
}
```

**Expected Response:**

```jsonc
{
  "message": "Review updated successfully"
}

// 200 OK
```

**Possible Status Codes:**

- 200 OK: When the review is successfully updated.
- 404 Not Found: If the review does not exist.
- 400 Bad Request: If input data is invalid.

## Authors
- **Fahad Alonazi** - [GitHub](https://github.com/Froot1)
- **Abdullatif Alzaher** - [GitHub](https://github.com/)
- **Abdulaziz Jumaiah** - [GitHub](https://github.com/)

