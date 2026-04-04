CREATE OR REPLACE FUNCTION search_contacts(p TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT c.id, c.name, c.phone FROM phonebook c
        WHERE c.name ILIKE '%' || p || '%'
           OR c.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, offs INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT c.id, c.name, c.phone FROM phonebook c
        ORDER BY c.id
        LIMIT lim OFFSET offs;
END;
$$ LANGUAGE plpgsql;