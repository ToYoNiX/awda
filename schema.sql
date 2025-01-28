CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    national_id_number TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birthday DATE NOT NULL,
    address TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    national_id_front TEXT NOT NULL,
    national_id_back TEXT NOT NULL,
    language TEXT DEFAULT 'en',
    theme TEXT DEFAULT 'light',
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);