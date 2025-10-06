-- Migration: Create Budgets Table
-- Created: 2025-01-06

CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    amount_limit REAL NOT NULL CHECK (amount_limit > 0),
    period VARCHAR(20) NOT NULL CHECK (period IN ('monthly', 'yearly')),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE,
    CHECK (end_date > start_date)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_budget_user ON budget(user_id);
CREATE INDEX IF NOT EXISTS idx_budget_category ON budget(category_id);
CREATE INDEX IF NOT EXISTS idx_budget_period ON budget(period);
CREATE INDEX IF NOT EXISTS idx_budget_dates ON budget(start_date, end_date);

-- Unique constraint to prevent duplicate budgets for same user/category/period
CREATE UNIQUE INDEX IF NOT EXISTS idx_budget_unique 
ON budget(user_id, category_id, period, start_date);
