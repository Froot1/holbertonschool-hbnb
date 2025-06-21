# TESTS

## USERS

### POST /api/v1/users/

**Registering a new user with valid informations**
```
curl -X 'POST' \
    'http://127.0.0.1:5000/api/v1/users/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "first_name": "Fahad",
    "last_name": "Alonazi",
    "email": "Fahad@example.com"
}'
```
Expected Response:
```
{
  "id": "489aa957-5cc4-45bc-91c2-d016310f40d7",
  "first_name": "Fahad",
  "last_name": "Alonazi",
  "email": "Fahad@example.com"
}
// 200 OK
```

**Non-valid email**
```
curl -X 'POST' \
    'http://127.0.0.1:5000/api/v1/users/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "first_name": "Fahad",
    "last_name": "Alonazi",
    "email": "Fahadexample.com"
}'
```
Expected Response:
```
{
  "error": "Invalid email format"
}
// 400 BAD REQUEST
```

**Already used email**
```
curl -X 'POST' \
    'http://127.0.0.1:5000/api/v1/users/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "first_name": "Fahad",
    "last_name": "Alonazi",
    "email": "Fahad@example.com"
}'
```
Expected Response:
```
{
  "error": "Email already registered"
}
// 400 BAD REQUEST
```

### GET /api/v1/users/

**Retrieving a list of all users**
```
curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/users/' \
  -H 'accept: application/json'
```
Expected Response:
```
[
  {
    "id": "489aa957-5cc4-45bc-91c2-d016310f40d7",
    "first_name": "Fahad",
    "last_name": "Alonazi",
    "email": "Fahad@example.com"
  },
  {
    "id": "4d1d3708-8b4a-4f47-b0ef-3574b3aac50a",
    "first_name": "user2",
    "last_name": "user2",
    "email": "valid@mail.com"
  }
]
// 200 OK
```

### GET /api/v1/users/{user_id}

**Retrieving a user with valid ID**
```
curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/users/4d1d3708-8b4a-4f47-b0ef-3574b3aac50a' \
  -H 'accept: application/json'
```
Expected Response:
```
{
  "id": "4d1d3708-8b4a-4f47-b0ef-3574b3aac50a",
  "first_name": "user2",
  "last_name": "user2",
  "email": "valid@mail.com"
}
// 200 OK
```

**Retrieving a user with invalid ID**
```
curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/users/thisisanid' \
  -H 'accept: application/json'
```
Expected Response:
```
{
  "error": "User not found"
}
// 400 BAD REQUEST
```

### PUT /api/v1/users/{user_id}

**Updating an user (user2) with valid informations and valid ID**
```
curl -X 'PUT' \
  'http://127.0.0.1:5000/api/v1/users/4d1d3708-8b4a-4f47-b0ef-3574b3aac50a' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Abdulaziz",
  "last_name": "Jumaiah",
  "email": "Abdulaziz@example.com"
}'
```
Expected Response:
```
{
  "id": "4d1d3708-8b4a-4f47-b0ef-3574b3aac50a",
  "first_name": "Abdulaziz",
  "last_name": "Jumaiah",
  "email": "Abdulaziz@example"
}
// 200 OK
```

**Non-valid ID**
```
curl -X 'PUT' \
  'http://127.0.0.1:5000/api/v1/users/thisisanid' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Abdulaziz",
  "last_name": "Jumaiah",
  "email": "Abdulaziz@example"
}'
```
Expected Response:
```
{
  "error": "User not found"
}
// 404 NOT FOUND
```

**Non-valid informations(mail)**
```
curl -X 'PUT' \
  'http://127.0.0.1:5000/api/v1/users/4d1d3708-8b4a-4f47-b0ef-3574b3aac50a' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Abdullatif",
  "last_name": "Alzaher",
  "email": "Abdullatif@examplecom"
}'
```
Expected Response:
```
{
  "error": "Invalid email format"
}
// 400 BAD REQUEST
```

**Non-valid informations(empty string)**
```
curl -X 'PUT' \
  'http://127.0.0.1:5000/api/v1/users/4d1d3708-8b4a-4f47-b0ef-3574b3aac50a' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "",
  "last_name": "",
  "email": "Abdullatif@example.com"
}'
```
Expected Response:
```
{
  "error": "First name must be provided and be less than 50 characters"
}
// 400 BAD REQUEST
```

## AMENITIES

### POST /api/v1/amenities/
**Creating a new amenity with a valid name**
```
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/amenities/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Swimming Pool"
}'
```
Expected Response:
```
{
  "id": "0c25aedf-fda9-4dd8-a6f6-10c3012d6d32",
  "name": "Swimming Pool"
}
// 200 OK
```

**testing with an empty string**
```
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/amenities/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": ""
}'
```
Expected Response:
```
{
  "error": "Name must be provided and be less than 50 characters"
}
// 400 BAD REQUEST
```

### GET /api/v1/amenities/
**Retrieving a list of all amenities**
```
curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/amenities/' \
  -H 'accept: application/json'
```
Expected Response:
```
[
  {
    "id": "0c25aedf-fda9-4dd8-a6f6-10c3012d6d32",
    "name": "Swimming Pool"
  },
  {
    "id": "2605b6b1-f662-46a0-9266-ff4be22a8ab5",
    "name": "Wi-Fi"
  }
]
// 200 OK
```

### GET /api/v1/amenities/{amenity_id}
**Retrieving an amenity by ID**
```
curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/amenities/0c25aedf-fda9-4dd8-a6f6-10c3012d6d32' \
  -H 'accept: application/json'
```
Expected Response:
```
{
  "id": "0c25aedf-fda9-4dd8-a6f6-10c3012d6d32",
  "name": "Swimming pool"
}
// 200 OK
```

**With an invalid ID**
```
curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/amenities/thisisanid' \
  -H 'accept: application/json'
```
Expected Response:
```
{
  "error": "Amenity not found"
}
// 404 NOT FOUND
```

### PUT /api/v1/amenities/{amenity_id}
**Updating an amenity with valid informations**
```
curl -X 'PUT' \
  'http://127.0.0.1:5000/api/v1/amenities/0c25aedf-fda9-4dd8-a6f6-10c3012d6d32' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Gym"
}'
```
Expected Response:
```
{
  "message": "Amenity updated successfully"
}
// 200 OK
```

**Updating an amenity with invalid informations(id)**
```
curl -X 'PUT' \
  'http://127.0.0.1:5000/api/v1/amenities/thisisanid' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Air conditioner"
}'
```
Expected Response:
```
{
  "error": "Amenity not found"
}
// 404 NOT FOUND
```

**Updating an amenity with invalid informations(empty string)**
```
curl -X 'PUT' \
  'http://127.0.0.1:5000/api/v1/amenities/0c25aedf-fda9-4dd8-a6f6-10c3012d6d32' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": ""
}'
```
Expected Response:
```
{
  "error": "Name must be provided and be less than 50 characters"
}
// 400 BAD REQUEST
```

## PLACES

### POST /api/v1/places/
**Creating a place with valid informations**
```
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/places/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Our Apartment",
  "description": "it'\''s really big",
  "price": 500,
  "latitude": 50.123,
  "longitude": 120.123,
  "owner_id": "3ada9273-4498-4f7e-b189-ddedd22071f6"
}'
```
Expected Response:
```
{
  "id": "3ada9273-4498-4f7e-b189-ddedd22071f6",
  "title": "Our Apartment",
  "description": "it's really big",
  "price": 500,
  "latitude": 50.123,
  "longitude": 120.123,
  "owner_id": "489aa957-5cc4-45bc-91c2-d016310f40d7"
}
// 201 CREATED
```

**Creating a place with an invalid user ID**
```
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/places/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Hotel",
  "description": "it'\''s Cool Place",
  "price": 200,
  "latitude": 40,
  "longitude": 50,
  "owner_id": "this is an id"
}'
```
Expected Response:
```
{
  "error": "Invalid owner_id"
}
// 400 BAD REQUEST
```

**Creating a place with an empty string**
```
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/places/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "",
  "description": "",
  "price": 1000,
  "latitude": 50,
  "longitude": 30,
  "owner_id": "489aa957-5cc4-45bc-91c2-d016310f40d7"
}'
```
Expected Response:
```
{
  "error": "Name must be provided and be less than 50 characters"
}
// 400 BAD REQUEST
```

### GET /api/v1/places/
**Retrieves a lsit of all places**
```
curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/places/' \
  -H 'accept: application/json'
```
Expected Response:
```
[
  {
    "id": "3ada9273-4498-4f7e-b189-ddedd22071f6",
    "title": "Our Apartment",
    "latitude": 50.123,
    "longitude": 120.123,
  },
  {
    "id": "da167086-426b-43a9-b8d6-4fc72fcdc1ba",
    "title": "Place 2",
    "latitude": 50,
    "longitude": 30,
  },
]
// 200 OK
```

### GET /api/v1/places/places/{place_id}/reviews

### GET /api/v1/places/{place_id}
**Retrieve a place with it's ID**
```
curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/places/3ada9273-4498-4f7e-b189-ddedd22071f6' \
  -H 'accept: application/json'
```
Expected Response:
```
{
  "id": "3ada9273-4498-4f7e-b189-ddedd22071f6",
  "title": "Our Apartment",
  "description": "it's really big",
  "price": 500,
  "latitude": 50.123,
  "longitude": 120.123,
  "owner": {
    "id": "489aa957-5cc4-45bc-91c2-d016310f40d7",
    "first_name": "Fahad",
    "last_name": "Alonazi",
    "email": "Fahad@example.com"
  },
  "amenities": []
}
// 200 OK
```

**Retrieve a place with an incorrect ID**
```
curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/places/thisisanid' \
  -H 'accept: application/json'
```
Expected Response:
```
{
  "error": "Place not found"
}
// 404 NOT FOUND
```

### PUT /api/v1/places/{place_id}

## REVIEWS

### POST /api/v1/reviews/
### GET /api/v1/reviews/
### GET /api/v1/reviews/{review_id}
### DELETE /api/v1/reviews/{review_id}
### PUT /api/v1/reviews/{review_id}

