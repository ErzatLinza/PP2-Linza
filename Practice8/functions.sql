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