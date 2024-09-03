CREATE DATABASE fitness_center;

USE fitness_center;

CREATE TABLE users(
id INT AUTO_INCREMENT PRIMARY KEY,
user_name VARCHAR(255) NOT NULL,
email VARCHAR(75) NOT NULL,
address VARCHAR(75) NOT NULL,
phone INT NOT NULL
);

SELECT * FROM users;
ALTER TABLE users MODIFY phone VARCHAR(15) NOT NULL;
INSERT INTO users (user_name, email, address, phone)
VALUES
('Tyler', 'tc@email.com', '123 fun St', '1234567890'),
('Brie', 'bf@email.com', '456 fun St', '9876543210');

CREATE TABLE workout_types (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL
);

INSERT INTO workout_types (type_name)
VALUES
('Chest'),
('Bicep'),
('Tricep'),
('Back'),
('Legs');

CREATE TABLE workout_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type_id INT NOT NULL,
    session_date DATE NOT NULL,
    duration INT,  -- duration in minutes
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (type_id) REFERENCES workout_types(type_id)
);

INSERT INTO workout_sessions (user_id, type_id, session_date, duration)
VALUES
(7, 1, '2024-09-01', 60),  
(8, 2, '2024-09-02', 45),  
(7, 5, '2024-09-03', 50);





