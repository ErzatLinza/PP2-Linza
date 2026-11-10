CREATE OR REPLACE PROCEDURE upsert_contact(
    p_username TEXT,
    p_phone TEXT,
    p_first_name TEXT DEFAULT NULL,
    p_surname TEXT DEFAULT NULL
)
AS $$
BEGIN
    IF p_username IS NULL
       OR length(trim(p_username)) NOT BETWEEN 1 AND 50 THEN
        RAISE EXCEPTION 'Username must contain 1-50 characters.';
    END IF;

    IF p_phone IS NULL
       OR trim(p_phone) !~ '^[+]?[0-9]{7,15}$' THEN
        RAISE EXCEPTION
            'Phone must contain 7-15 digits, optionally starting with +.';
    END IF;

    IF p_first_name IS NOT NULL
       AND length(trim(p_first_name)) NOT BETWEEN 1 AND 100 THEN
        RAISE EXCEPTION 'First name must contain 1-100 characters.';
    END IF;

    IF p_surname IS NOT NULL
       AND length(trim(p_surname)) > 100 THEN
        RAISE EXCEPTION 'Surname must contain at most 100 characters.';
    END IF;

    INSERT INTO contacts AS c (
        username, first_name, surname, phone
    )
    VALUES (
        trim(p_username),
        COALESCE(trim(p_first_name), trim(p_username)),
        COALESCE(trim(p_surname), ''),
        trim(p_phone)
    )
    ON CONFLICT (username) DO UPDATE
    SET phone = EXCLUDED.phone,
        first_name = COALESCE(trim(p_first_name), c.first_name),
        surname = COALESCE(trim(p_surname), c.surname);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_username TEXT[],
    p_phones TEXT[],
    INOUT incorrect_data JSONB DEFAULT '[]'::JSONB
)
AS $$
DECLARE
    entry RECORD;
    reason TEXT;
BEGIN
    incorrect_data := '[]'::JSONB;

    IF p_username IS NULL OR p_phones IS NULL THEN
        RAISE EXCEPTION 'Both lists are required.';
    END IF;

    IF cardinality(p_username) <> cardinality(p_phones) THEN
        RAISE EXCEPTION 'The lists must have the same length.';
    END IF;

    FOR entry IN
        SELECT *
        FROM unnest(p_username, p_phones)
        WITH ORDINALITY AS u(username, phone, position)
    LOOP
        reason := NULL;

        IF entry.username IS NULL
           OR length(trim(entry.username)) NOT BETWEEN 1 AND 50 THEN
            reason := 'Username must contain 1-50 characters.';

        ELSIF entry.phone IS NULL
           OR trim(entry.phone) !~ '^[+]?[0-9]{7,15}$' THEN
            reason := 'Phone must contain 7-15 digits, optionally starting with +.';

        ELSE
            BEGIN
                CALL upsert_contact(entry.username, entry.phone);

            EXCEPTION
                WHEN unique_violation THEN
                    reason := 'Phone already belongs to another username.';

                WHEN check_violation
                     OR not_null_violation
                     OR string_data_right_truncation THEN
                    reason := SQLERRM;
            END;
        END IF;

        IF reason IS NOT NULL THEN
            incorrect_data := incorrect_data ||
                jsonb_build_array(
                    jsonb_build_object(
                        'position', entry.position,
                        'username', entry.username,
                        'phone', entry.phone,
                        'reason', reason
                    )
                );
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE delete_contact(
    p_field TEXT,
    p_value TEXT,
    INOUT deleted_count INTEGER DEFAULT 0
)
AS $$
BEGIN
    IF p_value IS NULL OR trim(p_value) = '' THEN
        RAISE EXCEPTION 'Enter a username or phone.';
    END IF;

    IF p_field = 'username' THEN
        DELETE FROM contacts
        WHERE username = trim(p_value);

    ELSIF p_field = 'phone' THEN
        DELETE FROM contacts
        WHERE phone = trim(p_value);

    ELSE
        RAISE EXCEPTION 'Choose username or phone.';
    END IF;

    GET DIAGNOSTICS deleted_count = ROW_COUNT;
END;
$$ LANGUAGE plpgsql;