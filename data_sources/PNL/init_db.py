import sqlite3
import json

def create_table(cursor):
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
        INSERT INTO pnl (company_id, date, revenue, cost_of_goods_sold, gross_profit, operating_expenses, net_profit)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('company_id'),
            item.get('date'),
            item.get('revenue'),
            item.get('cost_of_goods_sold'),
            item.get('gross_profit'),
            item.get('operating_expenses'),
            item.get('net_profit')
        ))
    print("Data inserted successfully.")

def main():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_table(cursor)
    insert_data_from_json(cursor, 'data.json')  # Ensure pnl_data.json is available in the Docker context

    conn.commit()
    print("Database committed successfully.")
    conn.close()
    print("Database connection closed.")


if __name__ == '__main__':
    main()
