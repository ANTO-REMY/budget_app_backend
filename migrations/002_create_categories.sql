-- Migration: Create Categories Table
-- Created: 2025-01-06

CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES category(id) ON DELETE CASCADE
);

-- Create index for faster parent lookups
CREATE INDEX IF NOT EXISTS idx_category_parent ON category(parent_id);

-- Insert default categories
INSERT OR IGNORE INTO category (id, name, parent_id) VALUES 
(1, 'Foods & Drinks', NULL),
(2, 'Shopping', NULL),
(3, 'Housing', NULL),
(4, 'Transport', NULL),
(5, 'Vehicle', NULL),
(6, 'Life & Entertainment', NULL),
(7, 'Communication and PC', NULL),
(8, 'Financial Expenses', NULL),
(9, 'Investments', NULL),
(10, 'Income', NULL),
(11, 'Others', NULL);
