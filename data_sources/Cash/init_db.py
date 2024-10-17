import sqlite3
import json

def create_table(cursor):
    """Create the cash_flow table if it does not exist."""
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cash_flow (
        company_id TEXT PRIMARY KEY,
        date TEXT,
        beginning_cash REAL,
        net_income REAL,
        non_cash_items REAL,
        depreciation REAL,
        amortization REAL,
        change_in_working_capital REAL,
        cash_raised_spent_on_debt REAL,
        cash_raised_spent_on_equity REAL,
        ending_cash REAL
    )
    ''')
    print("Table created successfully.")

def insert_data_from_json(cursor, json_file):
    """Insert data into the cash_flow table from a JSON file."""
    with open(json_file) as f:
        data = json.load(f)
    
    # Clear existing data
    cursor.execute('DELETE FROM cash_flow')
    print("Existing data cleared.")

    # Insert new data
    for item in data:
        cursor.execute('''
        INSERT INTO cash_flow (company_id, date, beginning_cash, net_income, non_cash_items, depreciation, amortization, change_in_working_capital, cash_raised_spent_on_debt, cash_raised_spent_on_equity, ending_cash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('company_id'),
            item.get('date'),
            item.get('beginning_cash'),
            item.get('net_income'),
            item.get('non_cash_items'),
            item.get('depreciation'),
            item.get('amortization'),
            item.get('change_in_working_capital'),
            item.get('cash_raised_spent_on_debt'),
            item.get('cash_raised_spent_on_equity'),
            item.get('ending_cash')
        ))
    print("Data inserted successfully.")

def main():
    """Main function to initialize the database and insert data."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_table(cursor)
    insert_data_from_json(cursor, 'cash.json')

    conn.commit()
    print("Database committed successfully.")
    conn.close()
    print("Database connection closed.")

if __name__ == '__main__':
    main()



