-- ======================================================
-- TaskFlow Database Schema
-- PostgreSQL
-- ======================================================

-- Drop tables if they already exist
DROP TABLE IF EXISTS project_members CASCADE;
DROP TABLE IF EXISTS activity_logs CASCADE;
DROP TABLE IF EXISTS workflows CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS users CASCADE;

---------------------------------------------------------
-- USERS TABLE
-- Stores registered user accounts
-- PostgreSQL: SERIAL auto-increment, UNIQUE constraint on email
---------------------------------------------------------

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'Member',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- PROJECTS TABLE
-- Stores project information
-- PostgreSQL: FOREIGN KEY with ON DELETE SET NULL,
--             DATE type for start/end dates
---------------------------------------------------------

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(150) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(30) DEFAULT 'Active',

    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- PROJECT MEMBERS TABLE (Junction Table)
-- Many-to-many relationship between users and projects
-- Allows multiple users to be assigned to a project
-- PostgreSQL: Composite PRIMARY KEY, FOREIGN KEYS with CASCADE
---------------------------------------------------------

CREATE TABLE project_members (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(30) DEFAULT 'Member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, user_id)
);

---------------------------------------------------------
-- TASKS TABLE
-- Stores individual tasks within projects
-- PostgreSQL: FOREIGN KEYS, DEFAULT values, TIMESTAMP
---------------------------------------------------------

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,

    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

    assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,

    title VARCHAR(200) NOT NULL,

    description TEXT,

    priority VARCHAR(20) DEFAULT 'Medium',

    status VARCHAR(30) DEFAULT 'To Do',

    due_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- WORKFLOW TABLE
-- Tracks task workflow stage transitions
-- PostgreSQL: FOREIGN KEYS, TIMESTAMP tracking
---------------------------------------------------------

CREATE TABLE workflows (

    id SERIAL PRIMARY KEY,

    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,

    current_stage VARCHAR(30) DEFAULT 'To Do',

    previous_stage VARCHAR(30),

    updated_by INTEGER REFERENCES users(id),

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- ACTIVITY LOG TABLE
-- Records all user actions for audit trail
-- PostgreSQL: FOREIGN KEYS, DEFAULT TIMESTAMP
---------------------------------------------------------

CREATE TABLE activity_logs (

    id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(id),

    task_id INTEGER REFERENCES tasks(id),

    action VARCHAR(255),

    activity_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------
-- INDEXES
-- PostgreSQL: Improves query performance on frequently
--             searched columns
---------------------------------------------------------

CREATE INDEX idx_user_email
ON users(email);

CREATE INDEX idx_project_status
ON projects(status);

CREATE INDEX idx_project_members_project
ON project_members(project_id);

CREATE INDEX idx_project_members_user
ON project_members(user_id);

CREATE INDEX idx_task_status
ON tasks(status);

CREATE INDEX idx_task_priority
ON tasks(priority);

CREATE INDEX idx_task_project
ON tasks(project_id);

CREATE INDEX idx_activity_user
ON activity_logs(user_id);

CREATE INDEX idx_activity_time
ON activity_logs(activity_time DESC);

---------------------------------------------------------
-- SAMPLE DATA
-- PostgreSQL: INSERT with DEFAULT values, INTERVAL for dates
---------------------------------------------------------

-- Create sample users (passwords are hashed using werkzeug.security.generate_password_hash)
-- Default passwords: admin123, john123, jane123, bob123
INSERT INTO users(full_name, email, password, role)
VALUES
('Admin User', 'admin@taskflow.com', 'scrypt:32768:8:1$ys1WmXwkePA1tS25$f7063542bebb71814d51f9d8c5e6fe2cf7eecc2f6dc614ad724749dd3bbc6006d33d289e96cb0f77641e2b62e03928f814bbea67655a3ee3c708fc4f639ad85f', 'Admin'),
('John Doe', 'john@taskflow.com', 'scrypt:32768:8:1$IsBw1vJ3XW5yqKbF$aa0779ec124a7df306601bdcef8ca48eb2f71da08a8f6b55c6deba6291a367e999b44499a675b6a80e6efc6298d636bc762ebb39630fc5d61e56bb996bdf2a9e', 'Member'),
('Jane Smith', 'jane@taskflow.com', 'scrypt:32768:8:1$KgS4J1s3KzNkhzQE$d3bc06e2f6909a37f67a05ed83a80d5d975ff3d8bb51757d8e68da1744f6c9536da862949b3d30c67cdd0ae07526c459a27d8c4c4da568303d22ffc4dc07fc15', 'Member'),
('Bob Wilson', 'bob@taskflow.com', 'scrypt:32768:8:1$XnxqfZv7HxlttYbQ$95223f5b29c63ed83cc7f69d611ecd0bd44c999659b71a804b89a303af3ffb4bafb02c46cba7e3af58850c5c4525bafe5ca91cd02edc2ac6c7bb8357c3bcf04e', 'Member');

-- Create sample projects
INSERT INTO projects
(project_name, description, start_date, status, created_by)
VALUES
(
    'TaskFlow Development',
    'Main project of TaskFlow - a full-stack project management application built with Flask and PostgreSQL.',
    CURRENT_DATE,
    'Active',
    1
),
(
    'Website Redesign',
    'Redesign the company website with modern UI/UX principles using Bootstrap 5.',
    CURRENT_DATE,
    'Active',
    1
),
(
    'Mobile App',
    'Develop a cross-platform mobile application using React Native.',
    CURRENT_DATE + INTERVAL '7 day',
    'On Hold',
    2
);

-- Assign members to projects
INSERT INTO project_members (project_id, user_id, role)
VALUES
(1, 1, 'Admin'),
(1, 2, 'Member'),
(1, 3, 'Member'),
(2, 1, 'Admin'),
(2, 3, 'Member'),
(2, 4, 'Member'),
(3, 2, 'Admin'),
(3, 4, 'Member');

-- Create sample tasks
INSERT INTO tasks
(
    project_id, assigned_to, title, description,
    priority, status, due_date
)
VALUES
(
    1, 1, 'Design Database',
    'Create PostgreSQL schema with proper foreign keys, indexes, and constraints.',
    'High', 'To Do',
    CURRENT_DATE + INTERVAL '7 day'
),
(
    1, 2, 'Implement Authentication',
    'Build user registration, login, and session management using Flask.',
    'High', 'In Progress',
    CURRENT_DATE + INTERVAL '5 day'
),
(
    1, 3, 'Create Dashboard',
    'Design and implement the main dashboard with statistics cards and charts.',
    'Medium', 'To Do',
    CURRENT_DATE + INTERVAL '10 day'
),
(
    2, 3, 'Design Homepage',
    'Create a modern homepage layout with hero section and feature cards.',
    'High', 'Review',
    CURRENT_DATE + INTERVAL '3 day'
),
(
    2, 4, 'Build Contact Form',
    'Implement a contact form with validation and email notifications.',
    'Medium', 'To Do',
    CURRENT_DATE + INTERVAL '7 day'
),
(
    3, 2, 'Setup React Native',
    'Initialize React Native project and configure development environment.',
    'High', 'Completed',
    CURRENT_DATE - INTERVAL '2 day'
);

-- Create workflow entries for tasks
INSERT INTO workflows (task_id, current_stage, updated_by)
VALUES
(1, 'To Do', 1),
(2, 'In Progress', 2),
(3, 'To Do', 3),
(4, 'Review', 3),
(5, 'To Do', 4),
(6, 'Completed', 2);

-- Log sample activities
INSERT INTO activity_logs (user_id, task_id, action)
VALUES
(1, 1, 'Created first task'),
(2, 2, 'Started working on authentication'),
(3, 4, 'Moved homepage design to review'),
(2, 6, 'Completed React Native setup'),
(1, NULL, 'User Login'),
(2, NULL, 'User Login'),
(3, NULL, 'User Login');