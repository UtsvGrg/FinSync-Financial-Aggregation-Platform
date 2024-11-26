import requests
import csv
from datetime import datetime
import json
import os
from difflib import get_close_matches
import google.generativeai as genai
import os
import re

def llm_caller2(prompt):
    genai.configure(api_key='AIzaSyDkBTAQmwJLA4omqfRp2DVVtzd56fKqtek')
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    print(response.text)
    return response.text

def llm_caller(prompt):
    genai.configure(api_key='AIzaSyDkBTAQmwJLA4omqfRp2DVVtzd56fKqtek')
    model = genai.GenerativeModel("gemini-1.5-pro")
    system_adder = '''I have three data sources balance_sheet, cash_flow and pnl. The schema for the data sources are:

    SCHEMA of pnl - (company_id, date, cost_of_goods_sold, operating_expenses, depreciation, amortization, interest_expense, taxes, net_income)
    SCHEMA of balance_sheet - (company_id, date, current_assets, cash, long_term_assets, current_liabilities, long_term_debt, common_stock, retained_earnings)
    SCHEMA of cash_flow - (company_id, date, beginning_cash, net_income, non_cash_items, depreciation, amortization, change_in_working_capital, cash_raised_spent_on_debt, cash_raised_spent_on_equity, ending_cash) 

    I am using these data sources to create a Information Integration Application and have used the following schema mapping for each sources. Where keys of each source represent the SCHEMA and the value corresponding to the key is what the USER QUERY on.

    SCHEMA MAPPING of pnl : {
            "cost_of_goods_sold": "revenue",
            "operating_expenses": "operating_expenses",
            "depreciation": "long_term_assets",
            "amortization": "amortization",
            "interest_expense": "cash_raised_spent_on_debt",
            "taxes": "taxes",
            "net_income": "net_income"
        }

    SCHEMA MAPPING of balance_sheet: {
            "current_assets": "ending_cash",
            "cash": "cash",
            "long_term_assets": "long_term_assets",
            "current_liabilities": "current_liabilities",
            "long_term_debt": "cash_raised_spent_on_debt",
            "common_stock": "cash_raised_spent_on_equity",
            "retained_earnings": "net_income"
        }

    SCHEMA MAPPING of cash_flow: {
            "beginning_cash": "ending_cash",
            "net_income": "net_income",
            "non_cash_items": "non_cash_items",
            "depreciation": "long_term_assets",
            "amortization": "amortization",
            "change_in_working_capital": "current_liabilities",
            "cash_raised_spent_on_debt": "cash_raised_spent_on_debt",
            "cash_raised_spent_on_equity": "cash_raised_spent_on_equity"
        }

    Now given a USER QUERY generate SQL queries for each data source in the following JSON template without any comments in the JSON:
    
    EXAMPLE QUERY: Generate SQL queries for pnl, balance_sheet and cash_flow corresponding to its SCHEMA for companies with ending cash greater than 1 lakh 10 thousand
    EXAMPLE ANSWER TEMPLATE - {'pnl': 'SELECT * FROM pnl', 'balance_sheet': 'SELECT * FROM balance_sheet WHERE current_assets > 110000', 'cash_flow_statement': 'SELECT * FROM cash_flow WHERE beginning_cash > 110000'}

    USER QUERY: Generate SQL queries for each sources with its schema in the mentioned template for'''
    response = model.generate_content(system_adder+prompt)
    print(response.text)
    pattern = r"```json\n(.*?)```"
    match = re.search(pattern, response.text, re.DOTALL) 

    if match: 
        json_output = match.group(1) 
        return json.loads(json_output)
    
    else: 
        print("No JSON found.")
        return None

config_path = os.path.join('aggregator', 'config.json')
final_columns = []

def check_container_health():
    container_urls = {
        "pnl": "http://localhost:5001/data",
        "balance_sheet": "http://localhost:5002/data", 
        "cash_flow_statement": "http://localhost:5003/data"
    }
    
    available_containers = []
    for container, url in container_urls.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                available_containers.append(container)
        except:
            continue
            
    print("Available containers: ", available_containers)
    return available_containers

def get_final_columns():
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        
    available_containers = check_container_health()
    columns = {'company_id', 'date'} # Always include these
    
    for container in available_containers:
        columns.update(set(config['schema_mapping'][container].values()))
        
    return sorted(list(columns))

def generate_queries():
    queries = {
        "pnl": "SELECT * FROM pnl WHERE cost_of_goods_sold > 100000",
        "balance_sheet": "SELECT * FROM balance_sheet WHERE current_assets > 50000",
        "cash_flow_statement": "SELECT * FROM cash_flow WHERE beginning_cash > 100000"
    }
    print("Queries generated for all data sources.")
    return queries

def federate_queries(queries):
    container_urls = {
        "pnl": "http://localhost:5001/query",
        "balance_sheet": "http://localhost:5002/query",
        "cash_flow_statement": "http://localhost:5003/query"
    }
    
    # Update final_columns with current schema mapping
    global final_columns
    final_columns = get_final_columns()
    print("Final columns obtained:", final_columns)

    results = {}
    for data_type, url in container_urls.items():
        query = queries[data_type]
        try:
            response = requests.get(f"{url}?q={query}")
            response.raise_for_status()  # Raise an exception for bad status codes
            results[data_type] = response.json()
            print(f"Data fetched successfully from {data_type}")
        except requests.RequestException as e:
            print(f"Error fetching data from {data_type}: {str(e)}")
            results[data_type] = []  # Empty list instead of error string to allow processing to continue
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {data_type}: {str(e)}")
            results[data_type] = []  # Empty list for JSON decode errors
        except Exception as e:
            print(f"Unexpected error from {data_type}: {str(e)}")
            results[data_type] = []  # Empty list for any other errors
    
    return results

def schema_mapping():
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    print("Schema mapping loaded from config.json")
    return config['schema_mapping']

def load_company_ids():
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    print(f"Loaded {len(config['company_ids'])} valid company IDs from config.json")
    return config['company_ids']

def find_closest_company_id(company_id, valid_company_ids):
    matches = get_close_matches(company_id, valid_company_ids, n=1, cutoff=0.6)
    return matches[0] if matches else None

def aggregate_results(results, schema_map):
    valid_company_ids = load_company_ids()
    aggregated_data = {}
    for container_name, data in results.items():
        process_data_type(container_name, data, aggregated_data, schema_map, valid_company_ids)
    return finalize_aggregated_data(aggregated_data, valid_company_ids)

def process_data_type(data_type, data, aggregated_data, schema_map, valid_company_ids):
    for item in data:
        company_id = process_company_id(item.get('company_id'), valid_company_ids)

        # if company_id != item.get('company_id'):
        #     print("For container:", data_type, " the company_id is: ", item.get('company_id'), " and the processed company_id is: ", company_id)
        
        item['company_id']=company_id

        if company_id is None:
            continue
        
        if company_id not in aggregated_data:
            aggregated_data[company_id] = {}
        
        process_item(item, company_id, data_type, aggregated_data, schema_map)

def process_company_id(original_company_id, valid_company_ids):
    if not original_company_id:
        return None
    company_id = find_closest_company_id(original_company_id, valid_company_ids)
    if company_id is None:
        print(f"Warning: No match found for company ID '{original_company_id}'")
        return None
    if company_id != original_company_id:
        print(f"Company ID corrected: '{original_company_id}' -> '{company_id}'")
    return company_id

def process_item(item, company_id, data_type, aggregated_data, schema_map):
    for key, value in item.items():
        mapped_key = schema_map[data_type].get(key, key)
        if mapped_key not in aggregated_data[company_id]:
            aggregated_data[company_id][mapped_key] = {'sum': 0, 'count': 0, 'value': None}
        update_aggregated_value(aggregated_data[company_id][mapped_key], value)

def update_aggregated_value(aggregated_value, value):
    if isinstance(value, (int, float)):
        aggregated_value['sum'] += value
        aggregated_value['count'] += 1
        aggregated_value['value'] = aggregated_value['sum'] / aggregated_value['count']
    elif aggregated_value['value'] is None:
        aggregated_value['value'] = value

def finalize_aggregated_data(aggregated_data, valid_company_ids):
    final_aggregated_data = []
    for company_id in valid_company_ids:
        if company_id in aggregated_data:
            final_data = {'company_id': company_id}
            final_data.update({key: value_dict['value'] for key, value_dict in aggregated_data[company_id].items()})
            final_aggregated_data.append(final_data)

    # print("Final Aggregated Data: ", final_aggregated_data)

    # Remove items missing any of the required final columns
    final_aggregated_data = [
        item for item in final_aggregated_data 
        if all(col in item for col in final_columns)
    ]
    
    print(f"Data aggregated for {len(final_aggregated_data)} companies")
    return final_aggregated_data

def write_to_csv(data, filename):
    if not data:
        print("No data to write to CSV")
        return None

    keys = set()
    for item in data:
        keys.update(item.keys())
    keys = ['company_id', 'date'] + sorted(key for key in keys if key not in ['company_id', 'date'])
    
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        for row in data:
            row_with_all_keys = {key: row.get(key, None) for key in keys}
            dict_writer.writerow(row_with_all_keys)
    
    print(f"Data written to {filename}")
    return 0
    

def main():
    print("Starting data aggregation process...")
    queries = generate_queries()
    results = federate_queries(queries)
    schema_map = schema_mapping()
    aggregated_results = aggregate_results(results, schema_map)

    for item in aggregated_results:
        original_company_id = item.get('company_id')
        if original_company_id:
            closest_company_id = find_closest_company_id(original_company_id, load_company_ids())
            if closest_company_id and closest_company_id != original_company_id:
                item['company_id'] = closest_company_id
                print(f"Company ID corrected: '{original_company_id}' -> '{closest_company_id}'")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/aggregated_results_{timestamp}.csv"
    
    write_to_csv(aggregated_results, filename)
    print("Data aggregation process completed.")

if __name__ == "__main__":
    main()












# <--------------------------------------------- After django is running --------------------------------------------->

# # main.py
# from operations.django_handler import process_frontend_data, send_results_to_frontend
# from operations.query_federation import generate_queries, federate_queries
# from operations.data_aggregation import aggregate_results
# import json

# def main(frontend_data):
#     print("Starting data aggregation process...")
    
#     # Process frontend data
#     processed_data = process_frontend_data(frontend_data)
    
#     # Generate and federate queries
#     queries = generate_queries(processed_data)
#     results = federate_queries(queries)
    
#     # Load schema mapping
#     with open('config.json', 'r') as config_file:
#         config = json.load(config_file)
#     schema_map = config['schema_mapping']
    
#     # Aggregate results
#     aggregated_results = aggregate_results(results, schema_map)
    
#     # Send results back to frontend
#     send_results_to_frontend(aggregated_results)
    
#     print("Data aggregation process completed.")

# if __name__ == "__main__":
#     # This is just for testing purposes
#     # In a real Django app, this would be called by a view
#     sample_frontend_data = {
#         "cogs_threshold": 150000,
#         "assets_threshold": 75000,
#         "cash_threshold": 120000
#     }
#     main(sample_frontend_data)