-- Database creation schema for Reference Structure API

CREATE DATABASE IF NOT EXISTS `Agentic_DB`;
USE `Agentic_DB`;

CREATE TABLE IF NOT EXISTS `employee_details` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `phone` VARCHAR(20) NOT NULL,
    `occupation` VARCHAR(100) DEFAULT NULL,
    `designation` VARCHAR(100) DEFAULT NULL,
    `salary` DECIMAL(12, 2) DEFAULT NULL,
    `city` VARCHAR(100) DEFAULT NULL,
    `marital_status` VARCHAR(30) DEFAULT NULL,
    `status` VARCHAR(20) DEFAULT 'active',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
