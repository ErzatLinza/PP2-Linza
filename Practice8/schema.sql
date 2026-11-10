CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
             CHECK(length(trim(username)) > 0),
    first_name VARCHAR(100) NOT NULL
             CHECK (length(trim(first_name)) > 0),
    phone VARCHAR(16) UNIQUE NOT NULL 
             CHECK (phone ~ '^[+]?[0-9]{7,15}$')
);

ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS surname VARCHAR(100) NOT NULL DEFAULT '';