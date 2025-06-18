## Project Structure

```
hbnb/
├── app/
│   ├── api/v1/            # Versioned API endpoints
│   ├── models/            # Business logic classes (User, Place, etc.)
│   ├── services/          # Facade for communication between layers
│   └── persistence/       # In-memory data repository (to be replaced by DB)
├── run.py                 # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## How to Run the Project

Install dependencies and start the Flask server:

```bash
pip install -r requirements.txt
python run.py
```

Visit: http://localhost:5000/api/v1/

## Business Logic Layer

The `models/` directory contains all core entities and relationships. Each model inherits from a shared `BaseModel` that provides UUIDs and timestamp management.

### Implemented Models

#### User

**Attributes:**
- `id`: UUID
- `first_name`, `last_name`: Max 50 characters, required
- `email`: Unique and valid format
- `is_admin`: Boolean (default: False)
- `created_at`, `updated_at`

**Validations:**
- Name length
- Email format

#### Place

**Attributes:**
- `title`: Max 100 characters
- `description`: Optional
- `price`: Positive float
- `latitude`, `longitude`: Valid coordinate range
- `owner`: Linked `User` instance
- `created_at`, `updated_at`

**Relationships:**
- One User → Many Places
- One Place → Many Reviews
- Many Places ↔ Many Amenities

#### Review

**Attributes:**
- `text`: Required
- `rating`: Integer (1 to 5)
- `place`: Linked `Place`
- `user`: Linked `User`
- `created_at`, `updated_at`

#### Amenity

**Attributes:**
- `name`: Max 50 characters
- `created_at`, `updated_at`

### Entity Relationships

- User to Place: One-to-many  
- Place to Review: One-to-many  
- Place to Amenity: Many-to-many (using a list of Amenity instances or IDs)

### BaseModel

All models inherit from `BaseModel`, which provides:
- `id`: A UUID string
- `created_at`: Timestamp on creation
- `updated_at`: Timestamp on modification
- `save()`: Updates the `updated_at` timestamp
- `update(data_dict)`: Updates object fields from a dictionary and calls `save()`

