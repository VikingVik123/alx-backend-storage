-- Write a SQL script that creates a table users following these requirements
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    country CHAR(2) NOT NULL DEFAULT 'US' CHECK (country IN ('US', 'CO', 'TN'))
);