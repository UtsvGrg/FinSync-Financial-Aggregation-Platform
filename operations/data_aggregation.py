# data_aggregation.py
import json
from difflib import get_close_matches

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

def find_closest_company_id(company_id, valid_company_ids):
    matches = get_close_matches(company_id, valid_company_ids, n=1, cutoff=0.6)
    return matches[0] if matches else None

def aggregate_results(results, schema_map):
    config = load_config()
    valid_company_ids = config['company_ids']
    aggregated_data = {}
    averaged_columns = {}
    
    for data_type, data in results.items():
        for item in data:
            original_company_id = item.get('company_id')
            if not original_company_id:
                continue
            
            company_id = find_closest_company_id(original_company_id, valid_company_ids)
            
            if company_id is None:
                print(f"Warning: No match found for company ID '{original_company_id}'")
                continue
            
            if company_id != original_company_id:
                print(f"Company ID corrected: '{original_company_id}' -> '{company_id}'")
            
            if company_id not in aggregated_data:
                aggregated_data[company_id] = {}
                averaged_columns[company_id] = set()
            
            for key, value in item.items():
                mapped_key = schema_map[data_type].get(key, key)
                
                if mapped_key not in aggregated_data[company_id]:
                    aggregated_data[company_id][mapped_key] = {'sum': 0, 'count': 0, 'value': None}
                
                if isinstance(value, (int, float)):
                    aggregated_data[company_id][mapped_key]['sum'] += value
                    aggregated_data[company_id][mapped_key]['count'] += 1
                    aggregated_data[company_id][mapped_key]['value'] = aggregated_data[company_id][mapped_key]['sum'] / aggregated_data[company_id][mapped_key]['count']
                    averaged_columns[company_id].add(mapped_key)
                elif aggregated_data[company_id][mapped_key]['value'] is None:
                    aggregated_data[company_id][mapped_key]['value'] = value

    final_aggregated_data = []
    for company_id in valid_company_ids:
        if company_id in aggregated_data:
            final_data = {'company_id': company_id}
            for key, value_dict in aggregated_data[company_id].items():
                final_data[key] = value_dict['value']
            final_aggregated_data.append(final_data)
    
    print(f"Data aggregated for {len(final_aggregated_data)} companies")
    return final_aggregated_data

