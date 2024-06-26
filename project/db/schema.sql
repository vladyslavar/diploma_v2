CREATE TABLE user_account (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE organization (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES user_account(id),
    owner_id INT NOT NULL
);

CREATE TABLE app (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    api_key VARCHAR(255) NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organization(id),
    organization_id INT NOT NULL
);

CREATE TABLE user_organization_access (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    organization_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user_account(id),
    FOREIGN KEY (organization_id) REFERENCES organization(id)
);

CREATE OR REPLACE FUNCTION ADD_ORGANIZATION_ACCESS()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_organization_access (user_id, organization_id)
    VALUES (NEW.owner_id, NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER add_organization_access_trigger
AFTER INSERT ON organization
FOR EACH ROW
EXECUTE FUNCTION ADD_ORGANIZATION_ACCESS();


CREATE OR REPLACE FUNCTION REMOVE_ORGANIZATION_ACCESS()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM user_organization_access
    WHERE organization_id = OLD.id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER remove_organization_access_trigger
BEFORE DELETE ON organization
FOR EACH ROW
EXECUTE FUNCTION REMOVE_ORGANIZATION_ACCESS();


-- CREATE TABLE common_events (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     description TEXT
-- );

-- CREATE TABLE common_event_for_app (
--     id SERIAL PRIMARY KEY,
--     common_event_id INT NOT NULL,
--     app_id INT NOT NULL,
--     created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (common_event_id) REFERENCES common_events(id),
--     FOREIGN KEY (app_id) REFERENCES app(id)
-- );

CREATE TABLE event (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    app_id INT NOT NULL,
    FOREIGN KEY (app_id) REFERENCES app(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE event_parameter (
    id SERIAL PRIMARY KEY,
    event_id INT NOT NULL,
    parameter_name VARCHAR(255) NOT NULL,
    parameter_value TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES event(id)
);
