CREATE TABLE handled_error (
    id SERIAL PRIMARY KEY,
    error_code INTEGER NOT NULL,
    error_message TEXT NOT NULL
);