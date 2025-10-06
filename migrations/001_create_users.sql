-- Migration: Create Users Table
-- Created: 2025-01-06

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster email lookups
CREATE INDEX IF NOT EXISTS idx_user_email ON user(email);

-- Insert sample data (optional)
-- INSERT INTO user (email, password_hash, first_name, last_name) 
-- VALUES ('admin@budgetter.com', 'hashed_password', 'Admin', 'User');
