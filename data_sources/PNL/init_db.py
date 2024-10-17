import sqlite3
import json

def create_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pnl (
        company_id TEXT PRIMARY KEY,
        date TEXT,
        cost_of_goods_sold REAL,
        operating_expenses REAL,
        depreciation REAL,
        amortization REAL,
        interest_expense REAL,
        taxes REAL,
        net_income REAL
    )
    ''')
    print("Table created successfully.")

def insert_data_from_json(cursor, json_file):
    with open(json_file) as f:
        data = json.load(f)
    
    # Clear existing data
    cursor.execute('DELETE FROM pnl')
    print("Existing data cleared.")
    
    # Insert new data
    for item in data:
        cursor.execute('''
        INSERT INTO pnl (company_id, date, cost_of_goods_sold, operating_expenses, depreciation, amortization, interest_expense, taxes, net_income)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('company_id'),
            item.get('date'),
            item.get('cost_of_goods_sold'),
            item.get('operating_expenses'),
            item.get('depreciation'),
            item.get('amortization'),
            item.get('interest_expense'),
            item.get('taxes'),
            item.get('net_income')
        ))
    print("Data inserted successfully.")

def main():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_table(cursor)
    insert_data_from_json(cursor, 'pnl.json')  # Changed from 'data.json' to 'pnl.json'

    conn.commit()
    print("Database committed successfully.")
    conn.close()
    print("Database connection closed.")

if __name__ == '__main__':
    main()
