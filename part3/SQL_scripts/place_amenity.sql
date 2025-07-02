CREATE TABLE place_amenity (
    _place_id CHAR(36) PRIMARY KEY,
    _amenity_id CHAR(36) PRIMARY KEY,
    FOREIGN KEY (_place_id) REFERENCES place(id),
    FOREIGN KEY (_amenity_id) REFERENCES amenity(id)
);

