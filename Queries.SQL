create database hr_portal;
use hr_portal;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    azure_oid VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    role ENUM('hr', 'reviewer', 'manager', 'admin', 'static') NOT NULL,
    department VARCHAR(100),
    is_external BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);