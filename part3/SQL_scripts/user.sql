CREATE TABLE users (
    id UUID PRIMARY KEY,
    _first_name VARCHAR(255),
    _last_name VARCHAR(255),
    _email VARCHAR(255) UNIQUE,
    _password VARCHAR(255),
    _is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

