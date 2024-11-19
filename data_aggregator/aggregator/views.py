from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .forms import QueryForm
from .backend_logic import federate_queries, schema_mapping, aggregate_results, write_to_csv
import os
from datetime import datetime
import csv
import json
from django.shortcuts import redirect

def download_csv(request, filename):
    file_path = os.path.join(r'aggregator\output', filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("File not found.", status=404)
def generate_query(container, form_data, mapping):
    query = f"SELECT * FROM {container} WHERE "
    conditions = []
    for field, mapped_field in mapping[container].items():
        if field in form_data and f'{field}_operator' in form_data:
            value = form_data[field]
            operator = form_data[f'{field}_operator']
            if value is not None and operator:
                conditions.append(f"{mapped_field} {operator} {value}")
            #else print("Give Correct Input")    
    if conditions:
        query += " AND ".join(conditions)
    else:
        query = f"SELECT * FROM {container} WHERE 1=0"

    return query    


def default_view(request):
    return redirect('/query/')
    
def query_view(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            revenue = form.cleaned_data['revenue']
            revenue_operator = form.cleaned_data['revenue_operator']

            operating_expenses = form.cleaned_data['operating_expenses']
            operating_expenses_operator = form.cleaned_data['operating_expenses_operator']

            long_term_assets = form.cleaned_data['long_term_assets']
            long_term_assets_operator = form.cleaned_data['long_term_assets_operator']

            amortization = form.cleaned_data['amortization']
            amortization_operator = form.cleaned_data['amortization_operator']

            cash_raised_spent_on_debt = form.cleaned_data['cash_raised_spent_on_debt']
            cash_raised_spent_on_debt_operator = form.cleaned_data['cash_raised_spent_on_debt_operator']

            taxes = form.cleaned_data['taxes']
            taxes_operator = form.cleaned_data['taxes_operator']

            net_income = form.cleaned_data['net_income']
            net_income_operator = form.cleaned_data['net_income_operator']

            ending_cash = form.cleaned_data['ending_cash']
            ending_cash_operator = form.cleaned_data['ending_cash_operator']

            cash = form.cleaned_data['cash']
            cash_operator = form.cleaned_data['cash_operator']

            current_liabilities = form.cleaned_data['current_liabilities']
            current_liabilities_operator = form.cleaned_data['current_liabilities_operator']

            cash_raised_spent_on_equity = form.cleaned_data['cash_raised_spent_on_equity']
            cash_raised_spent_on_equity_operator = form.cleaned_data['cash_raised_spent_on_equity_operator']

            non_cash_items = form.cleaned_data['non_cash_items']
            non_cash_items_operator = form.cleaned_data['non_cash_items_operator']
            input_form = {
                'revenue': revenue,
                'revenue_operator': revenue_operator,
                'operating_expenses': operating_expenses,
                'operating_expenses_operator': operating_expenses_operator,
                'long_term_assets': long_term_assets,
                'long_term_assets_operator': long_term_assets_operator,
                'amortization': amortization,
                'amortization_operator': amortization_operator,
                'cash_raised_spent_on_debt': cash_raised_spent_on_debt,
                'cash_raised_spent_on_debt_operator': cash_raised_spent_on_debt_operator,
                'taxes': taxes,
                'taxes_operator': taxes_operator,
                'net_income': net_income,
                'net_income_operator': net_income_operator,
                'ending_cash': ending_cash,
                'ending_cash_operator': ending_cash_operator,
                'cash': cash,
                'cash_operator': cash_operator,
                'current_liabilities': current_liabilities,
                'current_liabilities_operator': current_liabilities_operator,
                'cash_raised_spent_on_equity': cash_raised_spent_on_equity,
                'cash_raised_spent_on_equity_operator':cash_raised_spent_on_equity_operator,
                'non_cash_items':non_cash_items,
                'non_cash_items_operator': non_cash_items_operator
            }
            field_mapping = {
                "pnl": {
                    "revenue": "cost_of_goods_sold",
                    "operating_expenses": "operating_expenses",
                    "amortization": "amortization",
                    "net_income": "net_income",
                    "cash_raised_spent_on_debt": "interest_expense",
                    "taxes": "taxes",
                    "long_term_assets": "depreciation"
                   
                },
                "balance_sheet": {
                    "ending_cash": "current_assets",
                    "cash": "cash",
                    "current_liabilities": "current_liabilities",
                    "long_term_assets": "long_term_assets",
                    "cash_raised_spent_on_debt": "long_term_debt",
                    "cash_raised_spent_on_equity": "common_stock",
                    "net_income": "retained_earnings"
                },
                "cash_flow": {
                    "ending_cash": "beginning_cash",
                    "net_income": "net_income",
                    "non_cash_items": "non_cash_items",
                    "long_term_assets": "depreciation",
                    "amortization": "amortization",
                    "current_liabilities": "change_in_working_capital",
                    "cash_raised_spent_on_debt": "cash_raised_spent_on_debt",
                    "cash_raised_spent_on_equity": "cash_raised_spent_on_equity"
                }
            }
            pnl_query = generate_query("pnl", input_form, field_mapping)
            balance_query = generate_query("balance_sheet", input_form, field_mapping)
            cash_query = generate_query("cash_flow", input_form, field_mapping)
            if "1=0" in pnl_query and "1=0" in cash_query and "1=0" in balance_query:
                print("hello")
                pnl_query="SELECT * FROM pnl"
                balance_query="SELECT * FROM balance_sheet"
                cash_query="SELECT * FROM cash_flow"
            print("Pnl:", pnl_query)
            print("Balance_Sheet:", balance_query)
            print("Cash_Flow:", cash_query)
         
            queries = {
                "pnl": pnl_query,
                "balance_sheet": balance_query,
                "cash_flow_statement": cash_query
            }
            results = federate_queries(queries)
            schema_map = schema_mapping()
            aggregated_results = aggregate_results(results, schema_map)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aggregated_results_{timestamp}.csv"
            output_path = os.path.join(r'aggregator/output', filename)
            if write_to_csv(aggregated_results, output_path) == None:
                output_path = os.path.join(r'aggregator/output', 'aggregated_results_empty.csv')
                print(output_path)

            csv_content = []
            with open(output_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    csv_content.append(row)
            return render(request, 'aggregator/query_form.html', {
                'form': form,
                'csv_content': csv_content,
                'headers': reader.fieldnames  # for table headers
            })

    else:
        form = QueryForm()

    return render(request, 'aggregator/query_form.html', {'form': form})
