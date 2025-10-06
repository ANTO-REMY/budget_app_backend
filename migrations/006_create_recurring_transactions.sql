-- Migration: Create Recurring Transactions Table
-- Created: 2025-01-06

CREATE TABLE IF NOT EXISTS recurring_transaction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    frequency VARCHAR(20) NOT NULL CHECK (frequency IN ('daily', 'weekly', 'monthly', 'yearly')),
    next_due_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    description VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_recurring_user ON recurring_transaction(user_id);
CREATE INDEX IF NOT EXISTS idx_recurring_category ON recurring_transaction(category_id);
CREATE INDEX IF NOT EXISTS idx_recurring_due_date ON recurring_transaction(next_due_date);
CREATE INDEX IF NOT EXISTS idx_recurring_active ON recurring_transaction(is_active);
CREATE INDEX IF NOT EXISTS idx_recurring_frequency ON recurring_transaction(frequency);

-- Create a view for due recurring transactions
CREATE VIEW IF NOT EXISTS due_recurring_transactions AS
SELECT 
    id,
    user_id,
    category_id,
    amount,
    type,
    frequency,
    next_due_date,
    description
FROM recurring_transaction 
WHERE is_active = 1 AND next_due_date <= DATE('now');
