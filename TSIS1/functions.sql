CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE(
    id INTEGER,
    username VARCHAR,
    first_name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.username, c.first_name, c.surname, c.phone
    FROM contacts AS c
    WHERE c.username ILIKE '%' || p_pattern || '%'
       OR c.first_name ILIKE '%' || p_pattern || '%'
       OR c.surname ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%'
    ORDER BY c.id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE(
    id INTEGER,
    username VARCHAR,
    first_name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    IF p_limit IS NULL OR p_limit <= 0
       OR p_offset IS NULL OR p_offset < 0 THEN
        RAISE EXCEPTION
            'LIMIT must be positive and OFFSET must be zero or positive.';
    END IF;

    RETURN QUERY
    SELECT c.id, c.username, c.first_name, c.surname, c.phone
    FROM contacts AS c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION sync_contact_phone()
RETURNS TRIGGER
AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        IF NEW.phone IS NOT DISTINCT FROM OLD.phone THEN
            RETURN NEW;
        END IF;

        IF EXISTS (
            SELECT 1
            FROM phones
            WHERE contact_id = NEW.id
              AND phone = NEW.phone
        ) THEN
            DELETE FROM phones
            WHERE contact_id = NEW.id
              AND phone = OLD.phone;

        ELSE
            UPDATE phones
            SET phone = NEW.phone
            WHERE contact_id = NEW.id
              AND phone = OLD.phone;
        END IF;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (NEW.id, NEW.phone, 'mobile')
    ON CONFLICT (contact_id, phone) DO NOTHING;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS contact_phone_sync ON contacts;

CREATE TRIGGER contact_phone_sync
AFTER INSERT OR UPDATE OF phone ON contacts
FOR EACH ROW
EXECUTE FUNCTION sync_contact_phone();

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INTEGER,
    username VARCHAR,
    first_name VARCHAR,
    surname VARCHAR,
    phone VARCHAR,
    email VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.username,
        c.first_name,
        c.surname,
        c.phone,
        c.email
    FROM contacts AS c
    WHERE c.username ILIKE '%' || p_query || '%'
       OR c.first_name ILIKE '%' || p_query || '%'
       OR c.surname ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR c.phone ILIKE '%' || p_query || '%'
       OR EXISTS (
            SELECT 1
            FROM phones AS p
            WHERE p.contact_id = c.id
              AND p.phone ILIKE '%' || p_query || '%'
       )
    ORDER BY c.id;
END;
$$ LANGUAGE plpgsql;