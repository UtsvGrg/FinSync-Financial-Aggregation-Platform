from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/data')
def get_data():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM cash_flow').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

@app.route('/query')
def execute_query():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    conn = get_db_connection()
    try:
        data = conn.execute(query).fetchall()
        return jsonify([dict(row) for row in data])
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
