import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS cash_flow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    company_id TEXT,
    cash_inflows_operating REAL,
    cash_outflows_operating REAL,
    cash_inflows_investing REAL,
    cash_outflows_investing REAL,
    cash_inflows_financing REAL,
    cash_outflows_financing REAL,
    net_cash_flow REAL
)
''')

# Insert mock data
cursor.execute('''
INSERT INTO cash_flow (date, cash_inflows_operating, cash_outflows_operating, cash_inflows_investing, cash_outflows_investing, cash_inflows_financing, cash_outflows_financing, net_cash_flow) VALUES
('2024-09-01', 6000.00, 3000.00, 2000.00, 1000.00, 1000.00, 500.00, 4500.00),
('2024-09-02', 7000.00, 3500.00, 2500.00, 1200.00, 1200.00, 600.00, 5600.00)
''')

conn.commit()
conn.close()
