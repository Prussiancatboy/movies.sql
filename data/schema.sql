CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    name TEXT,
    director TEXT,
    year INTEGER,
    rating TEXT,
    poster TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);