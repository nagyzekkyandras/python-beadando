USE app_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(15),
    title VARCHAR(20),
    team VARCHAR(20)
);

CREATE TABLE workday_locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    work_date DATE NOT NULL,
    location ENUM('Office', 'Home Office', 'Other') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


/* teszt adat, pw tesztelek */
INSERT INTO users (name, email, password, phone, title, team) VALUES ('User1', 'user1@example.com', 'pbkdf2:sha256:1000000$H6GugfO63mcDgtXb$d01bfd473b15ebe2c7c8860e8769b580672dea22f1e14822f0258ec88146edfa', '545876059', 'Coordinator', 'Product');
INSERT INTO users (name, email, password, phone, title, team) VALUES ('User2', 'user2@example.com', 'pbkdf2:sha256:1000000$H6GugfO63mcDgtXb$d01bfd473b15ebe2c7c8860e8769b580672dea22f1e14822f0258ec88146edfa', '740950763', 'Engineer', 'Development');
INSERT INTO users (name, email, password, phone, title, team) VALUES ('User3', 'user3@example.com', 'pbkdf2:sha256:1000000$H6GugfO63mcDgtXb$d01bfd473b15ebe2c7c8860e8769b580672dea22f1e14822f0258ec88146edfa', '846951270', 'Manager', 'HR');
INSERT INTO users (name, email, password, phone, title, team) VALUES ('User4', 'user4@example.com', 'pbkdf2:sha256:1000000$H6GugfO63mcDgtXb$d01bfd473b15ebe2c7c8860e8769b580672dea22f1e14822f0258ec88146edfa', '382140957', 'Specialist', 'Marketing');
INSERT INTO users (name, email, password, phone, title, team) VALUES ('User5', 'user5@example.com', 'pbkdf2:sha256:1000000$H6GugfO63mcDgtXb$d01bfd473b15ebe2c7c8860e8769b580672dea22f1e14822f0258ec88146edfa', '650987321', 'Analyst', 'Sales');
INSERT INTO users (name, email, password, phone, title, team) VALUES ('User6', 'user6@example.com', 'pbkdf2:sha256:1000000$H6GugfO63mcDgtXb$d01bfd473b15ebe2c7c8860e8769b580672dea22f1e14822f0258ec88146edfa', '712456839', 'Engineer', 'Development');
INSERT INTO users (name, email, password, phone, title, team) VALUES ('User7', 'user7@example.com', 'pbkdf2:sha256:1000000$H6GugfO63mcDgtXb$d01bfd473b15ebe2c7c8860e8769b580672dea22f1e14822f0258ec88146edfa', '934857612', 'Coordinator', 'Product');
INSERT INTO users (name, email, password, phone, title, team) VALUES ('User8', 'user8@example.com', 'pbkdf2:sha256:1000000$H6GugfO63mcDgtXb$d01bfd473b15ebe2c7c8860e8769b580672dea22f1e14822f0258ec88146edfa', '481230756', 'Manager', 'HR');
INSERT INTO users (name, email, password, phone, title, team) VALUES ('User9', 'user9@example.com', 'pbkdf2:sha256:1000000$H6GugfO63mcDgtXb$d01bfd473b15ebe2c7c8860e8769b580672dea22f1e14822f0258ec88146edfa', '509372864', 'Specialist', 'Marketing');
INSERT INTO users (name, email, password, phone, title, team) VALUES ('User10', 'user10@example.com', 'pbkdf2:sha256:1000000$H6GugfO63mcDgtXb$d01bfd473b15ebe2c7c8860e8769b580672dea22f1e14822f0258ec88146edfa', '675890432', 'Analyst', 'Sales');


INSERT INTO workday_locations (user_id, work_date, location) VALUES (1, CURRENT_DATE, 'Home Office');
INSERT INTO workday_locations (user_id, work_date, location) VALUES (2, CURRENT_DATE, 'Office');
INSERT INTO workday_locations (user_id, work_date, location) VALUES (3, CURRENT_DATE, 'Other');
INSERT INTO workday_locations (user_id, work_date, location) VALUES (4, CURRENT_DATE, 'Office');
INSERT INTO workday_locations (user_id, work_date, location) VALUES (5, CURRENT_DATE, 'Home Office');
INSERT INTO workday_locations (user_id, work_date, location) VALUES (6, CURRENT_DATE, 'Office');
INSERT INTO workday_locations (user_id, work_date, location) VALUES (7, CURRENT_DATE, 'Other');
INSERT INTO workday_locations (user_id, work_date, location) VALUES (8, CURRENT_DATE, 'Office');
INSERT INTO workday_locations (user_id, work_date, location) VALUES (9, CURRENT_DATE, 'Home Office');
INSERT INTO workday_locations (user_id, work_date, location) VALUES (10, CURRENT_DATE, 'Office');