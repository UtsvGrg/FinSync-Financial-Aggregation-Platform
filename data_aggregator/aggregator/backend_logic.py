import requests
import csv
from datetime import datetime
import json
from difflib import get_close_matches

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

def schema_mapping():
    with open(r'aggregator/config.json', 'r') as config_file:
        config = json.load(config_file)
    print("Schema mapping loaded from config.json")
    return config['schema_mapping']

def load_company_ids():
    with open(r'aggregator/config.json', 'r') as config_file:
        config = json.load(config_file)
    print(f"Loaded {len(config['company_ids'])} valid company IDs from config.json")
    return config['company_ids']

def find_closest_company_id(company_id, valid_company_ids):
    matches = get_close_matches(company_id, valid_company_ids, n=1, cutoff=0.6)
    return matches[0] if matches else None

def aggregate_results(results, schema_map):
    valid_company_ids = load_company_ids()
    aggregated_data = {}
    
    for data_type, data in results.items():
        process_data_type(data_type, data, aggregated_data, schema_map, valid_company_ids)
    
    return finalize_aggregated_data(aggregated_data, valid_company_ids)

def process_data_type(data_type, data, aggregated_data, schema_map, valid_company_ids):
    for item in data:
        company_id = process_company_id(item.get('company_id'), valid_company_ids)
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
    print(f"Data aggregated for {len(final_aggregated_data)} companies")
    return final_aggregated_data

def write_to_csv(data, filename):
    if not data:
        print("No data to write to CSV")
        return None

    keys = set()
    for item in data:
        keys.update(item.keys())
    print(keys)
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