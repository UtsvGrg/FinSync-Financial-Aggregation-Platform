import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS pnl (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT,
    date TEXT,
    revenue REAL,
    cost_of_goods_sold REAL,
    gross_profit REAL,
    operating_expenses REAL,
    net_profit REAL
)
''')

# Insert mock data
cursor.execute('''
INSERT INTO pnl (date, revenue, cost_of_goods_sold, gross_profit, operating_expenses, net_profit) VALUES
('2024-09-01', 12000.00, 3000.00, 9000.00, 5000.00, 4000.00),
('2024-09-02', 15000.00, 3500.00, 11500.00, 5500.00, 6000.00)
''')

conn.commit()
conn.close()
