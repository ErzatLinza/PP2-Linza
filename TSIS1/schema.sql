-- 1. Create contact categories.
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;


-- 2. Add the new contact fields.
ALTER TABLE contacts
    ADD COLUMN IF NOT EXISTS email VARCHAR(100),
    ADD COLUMN IF NOT EXISTS birthday DATE,
    ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id),
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ;


-- Record the date added for future contacts.
-- Existing contacts keep NULL because their original dates are unknown.
ALTER TABLE contacts
    ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;


-- Put existing uncategorized contacts into Other.
UPDATE contacts
SET group_id = (
    SELECT id FROM groups WHERE name = 'Other'
)
WHERE group_id IS NULL;


-- 3. Create a separate table for multiple phone numbers.
CREATE TABLE IF NOT EXISTS phones (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    contact_id INTEGER NOT NULL
        REFERENCES contacts(id) ON DELETE CASCADE,

    phone VARCHAR(20) NOT NULL
        CHECK (phone ~ '^[+]?[0-9]{7,15}$'),

    type VARCHAR(10) NOT NULL
        CHECK (type IN ('home', 'work', 'mobile')),

    UNIQUE (contact_id, phone)
);


-- 4. Copy existing numbers into the new table.
INSERT INTO phones (contact_id, phone, type)
SELECT id, phone, 'mobile'
FROM contacts
ON CONFLICT (contact_id, phone) DO NOTHING;