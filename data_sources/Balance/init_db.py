import sqlite3
import json
import os

def create_table(cursor):
    print("Creating balance_sheet table...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS balance_sheet (
        company_id TEXT PRIMARY KEY,
        date TEXT,
        current_assets REAL,
        cash REAL,
        long_term_assets REAL,
        current_liabilities REAL,
        long_term_debt REAL,
        common_stock REAL,
        retained_earnings REAL
    )
    ''')
    print("Table created successfully.")

def fetch_json_data(json_file):
    print(f"Current working directory: {os.getcwd()}")
    print(f"Attempting to open file: {json_file}")
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        print(f"Successfully loaded data from {json_file}")
        print(f"Number of items in JSON: {len(data)}")
        return data
    except FileNotFoundError:
        print(f"Error: File {json_file} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File {json_file} is not valid JSON.")
        return None

def clear_table(cursor):
    print("Clearing existing data from balance_sheet table...")
    cursor.execute('DELETE FROM balance_sheet')
    print("Table cleared successfully.")

def insert_data(cursor, data):
    print("Inserting new data into balance_sheet table...")
    for item in data:
        try:
            # Validate data types before insertion
            validated_data = {
                'company_id': str(item.get('company_id', '')),  # Ensure string
                'date': str(item.get('date', '')),  # Ensure string
                'current_assets': float(item.get('current_assets', 0) or 0),  # Convert to float or 0
                'cash': float(item.get('cash', 0) or 0),
                'long_term_assets': float(item.get('long_term_assets', 0) or 0),
                'current_liabilities': float(item.get('current_liabilities', 0) or 0),
                'long_term_debt': float(item.get('long_term_debt', 0) or 0),
                'common_stock': float(item.get('common_stock', 0) or 0),
                'retained_earnings': float(item.get('retained_earnings', 0) or 0)
            }

            cursor.execute('''
            INSERT INTO balance_sheet (company_id, date, current_assets, cash, long_term_assets, 
                                     current_liabilities, long_term_debt, common_stock, retained_earnings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                validated_data['company_id'],
                validated_data['date'],
                validated_data['current_assets'],
                validated_data['cash'],
                validated_data['long_term_assets'],
                validated_data['current_liabilities'],
                validated_data['long_term_debt'],
                validated_data['common_stock'],
                validated_data['retained_earnings']
            ))
            print(f"Inserted item: {validated_data}")
        except (ValueError, TypeError) as e:
            print(f"Data type error in item: {item}. Error: {e}")
            continue  # Skip this record but continue processing others
        except sqlite3.Error as e:
            print(f"Database error inserting item: {item}. Error: {e}")
            continue
    
    print(f"Inserted {cursor.rowcount} rows into the database.")

def main():
    print("Starting database initialization...")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_table(cursor)
    
    json_data = fetch_json_data('balance.json')
    if json_data is not None:
        clear_table(cursor)
        insert_data(cursor, json_data)
    
    conn.commit()
    print("Changes committed to database.")
    conn.close()
    print("Database connection closed.")
    print("Database initialization complete.")

if __name__ == '__main__':
    main()
