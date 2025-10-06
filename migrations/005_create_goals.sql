-- Migration: Create Goals Table
-- Created: 2025-01-06

CREATE TABLE IF NOT EXISTS goal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(100) NOT NULL,
    target_amount REAL NOT NULL CHECK (target_amount > 0),
    current_amount REAL DEFAULT 0.0 CHECK (current_amount >= 0),
    target_date DATE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'paused')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    CHECK (current_amount <= target_amount)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_goal_user ON goal(user_id);
CREATE INDEX IF NOT EXISTS idx_goal_status ON goal(status);
CREATE INDEX IF NOT EXISTS idx_goal_target_date ON goal(target_date);

-- Create a view for goal progress
CREATE VIEW IF NOT EXISTS goal_progress AS
SELECT 
    id,
    user_id,
    title,
    target_amount,
    current_amount,
    ROUND((current_amount * 100.0 / target_amount), 2) as progress_percentage,
    target_date,
    status,
    created_at
FROM goal;
