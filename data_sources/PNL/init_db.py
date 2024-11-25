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
        try:
            # Validate data types before insertion
            validated_data = {
                'company_id': str(item.get('company_id', '')),  # Ensure string
                'date': str(item.get('date', '')),  # Ensure string
                'cost_of_goods_sold': float(item.get('cost_of_goods_sold', 0)),  # Ensure float
                'operating_expenses': float(item.get('operating_expenses', 0)),
                'depreciation': float(item.get('depreciation', 0)),
                'amortization': float(item.get('amortization', 0)), 
                'interest_expense': float(item.get('interest_expense', 0)),
                'taxes': float(item.get('taxes', 0)),
                'net_income': float(item.get('net_income', 0))
            }

            cursor.execute('''
            INSERT INTO pnl (company_id, date, cost_of_goods_sold, operating_expenses, depreciation, amortization, interest_expense, taxes, net_income)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                validated_data['company_id'],
                validated_data['date'],
                validated_data['cost_of_goods_sold'],
                validated_data['operating_expenses'], 
                validated_data['depreciation'],
                validated_data['amortization'],
                validated_data['interest_expense'],
                validated_data['taxes'],
                validated_data['net_income']
            ))
        except (ValueError, TypeError) as e:
            print(f"Error validating data for company {item.get('company_id')}: {e}")
            continue
            
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
