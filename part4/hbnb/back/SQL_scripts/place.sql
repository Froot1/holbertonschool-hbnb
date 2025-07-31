CREATE TABLE place (
    id UUID PRIMARY KEY,
    _title VARCHAR(255),
    _description TEXT,
    _price DECIMAL(10, 2),
    _latitude FLOAT,
    _longitude FLOAT,
    _owner_id CHAR(36),
    FOREIGN KEY (_owner_id) REFERENCES user(id)
);

