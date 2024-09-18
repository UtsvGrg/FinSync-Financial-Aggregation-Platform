import sqlite3
import json

def create_table(cursor):
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

def insert_data_from_json(cursor, json_file):
    with open(json_file) as f:
        data = json.load(f)
    
    # Clear existing data
    cursor.execute('DELETE FROM balance_sheet')

    # Insert new data
    for item in data:
        cursor.execute('''
        INSERT INTO balance_sheet (id, company_id, date, assets_current, assets_non_current, liabilities_current, liabilities_non_current, equity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('id'),
            item.get('company_id'),
            item.get('date'),
            item.get('assets_current'),
            item.get('assets_non_current'),
            item.get('liabilities_current'),
            item.get('liabilities_non_current'),
            item.get('equity')
        ))

def main():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_table(cursor)
    insert_data_from_json(cursor, 'balance.json')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
