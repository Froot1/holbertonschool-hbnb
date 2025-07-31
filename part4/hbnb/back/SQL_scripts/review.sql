CREATE TABLE review (
    id UUID PRIMARY KEY,
    _text TEXT,
    _rating INT CHECK (_rating BETWEEN 1 AND 5),
    _user_id CHAR(36) UNIQUE,
    _place_id CHAR(36) UNIQUE,
    FOREIGN KEY (_user_id) REFERENCES user(id),
    FOREIGN KEY (_place_id) REFERENCES place(id)
);

