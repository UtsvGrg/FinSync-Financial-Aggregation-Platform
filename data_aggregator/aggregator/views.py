from django.shortcuts import render
from .forms import QueryForm
from .backend_logic import federate_queries, schema_mapping, aggregate_results, write_to_csv, llm_caller, llm_caller2
import os
from datetime import datetime
import csv
from django.shortcuts import redirect
    
def generate_query(container, form_data, mapping):
    '''Working: Generates a SQL query based on the form data and mapping.
    
    Args:
        container: Name of the data container (pnl, balance_sheet, cash_flow)
        form_data: Dictionary of form data
        mapping: Dictionary of field mappings
        
    Returns:
        str: SQL query
    '''
    query = f"SELECT * FROM {container} WHERE "
    conditions = []
    for field, mapped_field in mapping[container].items():
        if field in form_data and f'{field}_operator' in form_data:
            value = form_data[field]
            operator = form_data[f'{field}_operator']
            if value is not None and operator:
                conditions.append(f"{mapped_field} {operator} {value}")
    if conditions:
        query += " AND ".join(conditions)
    else:
        query = f"SELECT * FROM {container}"

    # print("For ", container, " the query is: ", query)
    return query    


def default_view(request):
    # llm_caller('Companies with amortization value greater than 1 lakh 10 thousand') 
    # llm_caller('Companies with amortization greater than 1 lakh 10 thousand and current liabilities less than 26k')
    # llm_caller('companies with operating expenses greater than 2500000.0')
    return redirect('/query/')

def jaccard_similarity(field1, field2):
    set1 = set(field1.lower())
    set2 = set(field2.lower())
    return len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0

def outer_schema_mapping():
    predefined_mapping= {
        "pnl": {
            "revenue": "cost_of_goods_sold",
            "operating_expenses": "operating_expenses",
            "long_term_assets": "depreciation",
            "amortization": "amortization",
            "cash_raised_spent_on_debt": "interest_expense",
            "taxes": "taxes",
            "net_income": "net_cash_amount" #----***jackard Applied****------
            
        },
        "balance_sheet": {
            "ending_cash": "current_assets",
            "cash": "cash_on_hand", #----***jackard Applied****------
            "long_term_assets": "long_term_assets",
            "current_liabilities": "current_liabilities",
            "cash_raised_spent_on_debt": "long_term_debt",
            "cash_raised_spent_on_equity": "common_stock",
            "net_income": "retained_earnings"
        },
        "cash_flow": {
            "ending_cash": "beginning_cash",
            "net_income": "net_amount",  #----***jackard Applied****------
            "non_cash_items": "non_cash_items",
            "long_term_assets": "depreciation",
            "amortization": "amortization",
            "current_liabilities": "change_in_working_capital",
            "cash_raised_spent_on_debt": "cash_raised_spent_on_debt",
            "cash_raised_spent_on_equity": "cash_raised_spent_on_equity"
        }
    }
    external_schema = {
        "pnl": ["cost_of_goods_sold","depreciation","operating_expenses","amortization", "net_income", "interest_expense","taxes"],
        "balance_sheet": ["current_assets", "cash", "current_liabilities","long_term_assets","long_term_debt","common_stock","retained_earnings"],
        "cash_flow": ["beginning_cash","net_income", "non_cash_items","depreciation","amortization","change_in_working_capital", "cash_raised_spent_on_debt", "cash_raised_spent_on_equity"]
    }
    for table, fields in external_schema.items():
        if table in predefined_mapping:
            for internal_field in predefined_mapping[table]:
                if predefined_mapping[table][internal_field] not in fields:
                    best_match = max(fields, key=lambda f: jaccard_similarity(internal_field, f))
                    if jaccard_similarity(internal_field, best_match) > 0.3: 
                        predefined_mapping[table][internal_field] = best_match                 
    return predefined_mapping

def query_view(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)

        if form.is_valid(): 

            input_form = {field: form.cleaned_data[field] for field in form.cleaned_data}
            print(input_form)

            field_mapping = outer_schema_mapping()
            print("***----Final Mapping after jackard Applied: ***----: ",field_mapping)
            pnl_query = generate_query("pnl", input_form, field_mapping)
            balance_query = generate_query("balance_sheet", input_form, field_mapping)
            cash_query = generate_query("cash_flow", input_form, field_mapping)
            print("Pnl_Query: ",pnl_query)
            print("balance_query: ",balance_query)
            print("cash_query",cash_query)
            
            queries = {
                "pnl": pnl_query,
                "balance_sheet": balance_query,
                "cash_flow_statement": cash_query
            }

            flag_var = False

            if input_form['llm_search']!="":
                flag_var = True
                queries = llm_caller(input_form['llm_search'])

            if queries!=None:
                #print("Queries: ", queries)
                results = federate_queries(queries)

                schema_map = schema_mapping()
                aggregated_results = aggregate_results(results, schema_map)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"aggregated_results_{timestamp}.csv"
                output_path = os.path.join(r'aggregator/output', filename)
                if write_to_csv(aggregated_results, output_path) == None:
                    output_path = os.path.join(r'aggregator/output', 'aggregated_results_empty.csv')
                    print(output_path)
            
            else:
                output_path = os.path.join(r'aggregator/output', 'aggregated_results_empty.csv')

            csv_content = []
            with open(output_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    csv_content.append(row)

            analysis_result = None
            print("INPUT", input_form['analysis_option'])
            if request.POST.get('llm_analysis') == 'true' and input_form['analysis_option']!='':
                print(aggregated_results)
                final_prompt = repr(aggregated_results) 
                final_prompt += 'This is a csv data of companies in the form of list, comment on' 
                final_prompt += input_form['analysis_option']
                final_prompt += 'and why?. All in just one paragraph'
                analysis_result = llm_caller2(final_prompt)

            return render(request, 'aggregator/query_form.html', {
                'form': form,
                'csv_content': csv_content,
                'analysis_result': analysis_result,
                'headers': reader.fieldnames  # for table headers

            })

    else:
        form = QueryForm()

    return render(request, 'aggregator/query_form.html', {'form': form, })
