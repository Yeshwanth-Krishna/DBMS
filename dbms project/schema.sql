CREATE DATABASE IF NOT EXISTS dbmsproj;
USE dbmsproj;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role ENUM('student', 'faculty', 'admin') NOT NULL
);
