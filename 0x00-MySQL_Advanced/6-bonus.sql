-- Write a SQL script that creates a stored procedure AddBonus
-- should add a new correction for a student
CREATE PROCEDURE AddBonus (
    user_id INTEGER
    project_name VARCHAR(255)
    SCORE INTEGER
)
BEGIN
    DECLARE project_id INT;

    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name

IF project_id IS NULL THEN
    INSERT INTO projects (name)
    VALUES (project_name);
    SET project_id = LAST_INSERT_ID();
END IF;

INSERT INTO corrections (user_id, project_id, score)
VALUES (user_id, project_id, score);
END;