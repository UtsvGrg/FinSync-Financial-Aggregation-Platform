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
        try:
            # Validate data types before insertion
            validated_data = {
                'company_id': str(item.get('company_id', '')),  # Ensure string
                'date': str(item.get('date', '')),  # Ensure string
                'beginning_cash': float(item.get('beginning_cash', 0)),  # Ensure float
                'net_income': float(item.get('net_income', 0)),
                'non_cash_items': float(item.get('non_cash_items', 0)),
                'depreciation': float(item.get('depreciation', 0)),
                'amortization': float(item.get('amortization', 0)),
                'change_in_working_capital': float(item.get('change_in_working_capital', 0)),
                'cash_raised_spent_on_debt': float(item.get('cash_raised_spent_on_debt', 0)),
                'cash_raised_spent_on_equity': float(item.get('cash_raised_spent_on_equity', 0)),
                'ending_cash': float(item.get('ending_cash', 0))
            }

            cursor.execute('''
            INSERT INTO cash_flow (company_id, date, beginning_cash, net_income, non_cash_items, depreciation, amortization, change_in_working_capital, cash_raised_spent_on_debt, cash_raised_spent_on_equity, ending_cash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                validated_data['company_id'],
                validated_data['date'], 
                validated_data['beginning_cash'],
                validated_data['net_income'],
                validated_data['non_cash_items'],
                validated_data['depreciation'],
                validated_data['amortization'],
                validated_data['change_in_working_capital'],
                validated_data['cash_raised_spent_on_debt'],
                validated_data['cash_raised_spent_on_equity'],
                validated_data['ending_cash']
            ))
        except (ValueError, TypeError) as e:
            print(f"Error validating data for company {item.get('company_id')}: {e}")
            continue
            
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



