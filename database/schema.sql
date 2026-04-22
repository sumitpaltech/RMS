-- ============================================================
--  TaskApp Database Schema
--  Drop and recreate cleanly
-- ============================================================

CREATE DATABASE IF NOT EXISTS `3IdeaTask` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `3IdeaTask`;

-- ----------------------------------------
-- Table: users
-- ----------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id         INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    name       VARCHAR(100)    NOT NULL,
    email      VARCHAR(150)    NOT NULL UNIQUE,
    password   VARCHAR(255)    NOT NULL,
    created_at DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------
-- Table: tasks
-- ----------------------------------------
CREATE TABLE IF NOT EXISTS tasks (
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    user_id     INT UNSIGNED    NOT NULL,
    title       VARCHAR(200)    NOT NULL,
    description TEXT,
    status      ENUM('pending','in_progress','completed') NOT NULL DEFAULT 'pending',
    priority    ENUM('low','medium','high')               NOT NULL DEFAULT 'medium',
    due_date    DATE,
    created_at  DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status  (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------
-- Seed: demo user  (password: password123)
-- ----------------------------------------
INSERT INTO users (name, email, password) VALUES
('Demo User', 'demo@example.com',
 'pbkdf2:sha256:600000$example$hashedpassword');
 -- Run `python seed.py` to insert a properly hashed user instead.

-- ----------------------------------------
-- Seed: sample tasks
-- ----------------------------------------
INSERT INTO tasks (user_id, title, description, status, priority, due_date) VALUES
(1, 'Setup project environment',  'Install Python, Flask, MySQL',    'completed',  'high',   '2024-01-10'),
(1, 'Design database schema',     'Create users and tasks tables',   'completed',  'high',   '2024-01-12'),
(1, 'Build auth system',          'Login, register, logout',         'in_progress','medium', '2024-01-20'),
(1, 'Build task CRUD',            'Create, read, update, delete',    'pending',    'high',   '2024-01-25'),
(1, 'Deploy to production',       'Setup server and go live',        'pending',    'low',    '2024-02-01');
