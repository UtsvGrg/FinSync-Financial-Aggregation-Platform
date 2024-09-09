import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS balance_sheet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT,
    date TEXT,
    assets_current REAL,
    assets_non_current REAL,
    liabilities_current REAL,
    liabilities_non_current REAL,
    equity REAL
)
''')

# Insert mock data
cursor.execute('''
INSERT INTO balance_sheet (date, assets_current, assets_non_current, liabilities_current, liabilities_non_current, equity) VALUES
('2024-09-01', 20000.00, 30000.00, 10000.00, 15000.00, 25000.00),
('2024-09-02', 21000.00, 31000.00, 10500.00, 15500.00, 26000.00)
''')

conn.commit()
conn.close()
