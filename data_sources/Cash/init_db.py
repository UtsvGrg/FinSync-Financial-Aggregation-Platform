import sqlite3
import json

def create_table(cursor):
    """Create the cash_flow table if it does not exist."""
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

def insert_data_from_json(cursor, json_file):
    """Insert data into the cash_flow table from a JSON file."""
    with open(json_file) as f:
        data = json.load(f)
    
    # Clear existing data
    cursor.execute('DELETE FROM cash_flow')

    # Insert new data
    for item in data:
        cursor.execute('''
        INSERT INTO cash_flow (date, company_id, cash_inflows_operating, cash_outflows_operating, cash_inflows_investing, cash_outflows_investing, cash_inflows_financing, cash_outflows_financing, net_cash_flow)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('date'),
            item.get('company_id'),
            item.get('cash_inflows_operating'),
            item.get('cash_outflows_operating'),
            item.get('cash_inflows_investing'),
            item.get('cash_outflows_investing'),
            item.get('cash_inflows_financing'),
            item.get('cash_outflows_financing'),
            item.get('net_cash_flow')
        ))

def main():
    """Main function to initialize the database and insert data."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_table(cursor)
    insert_data_from_json(cursor, 'cash.json')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()


