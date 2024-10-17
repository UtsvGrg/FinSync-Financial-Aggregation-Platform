# query_federation.py
import requests

def generate_queries(data):
    # Generate queries based on frontend data
    queries = {
        "pnl": f"SELECT * FROM pnl WHERE cost_of_goods_sold > {data.get('cogs_threshold', 100000)}",
        "balance_sheet": f"SELECT * FROM balance_sheet WHERE current_assets > {data.get('assets_threshold', 50000)}",
        "cash_flow_statement": f"SELECT * FROM cash_flow WHERE beginning_cash > {data.get('cash_threshold', 100000)}"
    }
    print("Queries generated for all data sources.")
    return queries

def federate_queries(queries):
    container_urls = {
        "pnl": "http://localhost:5001/query",
        "balance_sheet": "http://localhost:5002/query",
        "cash_flow_statement": "http://localhost:5003/query"
    }
    
    results = {}
    for data_type, url in container_urls.items():
        query = queries[data_type]
        try:
            response = requests.get(f"{url}?q={query}")
            results[data_type] = response.json()
            print(f"Data fetched successfully from {data_type}")
        except requests.RequestException as e:
            results[data_type] = f"Error: {str(e)}"
            print(f"Error fetching data from {data_type}: {str(e)}")
    
    return results
