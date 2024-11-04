from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .forms import QueryForm
from .backend_logic import federate_queries, schema_mapping, aggregate_results, write_to_csv
import os
from datetime import datetime
import csv

# aggregator/views.py
def download_csv(request, filename):
    file_path = os.path.join(r'aggregator\output', filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("File not found.", status=404)


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

            print(revenue_operator)
            print(revenue)

            ## Generate the following queries from the data recieved from above
            pnl_query = "SELECT * FROM pnl WHERE cost_of_goods_sold > 100000"
            balance_query = "SELECT * FROM balance_sheet WHERE current_assets > 50000"
            cash_query = "SELECT * FROM cash_flow WHERE beginning_cash > 100000"

            queries = {
                "pnl": pnl_query,
                "balance_sheet": balance_query,
                "cash_flow_statement": cash_query
            }

            # Federate queries and process results
            results = federate_queries(queries)
            schema_map = schema_mapping()
            aggregated_results = aggregate_results(results, schema_map)

            # Generate filename and write to CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aggregated_results_{timestamp}.csv"
            output_path = os.path.join(r'aggregator\output', filename)
            write_to_csv(aggregated_results, output_path)

            csv_content = []
            with open(output_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    csv_content.append(row)

            # Pass the CSV content to the template
            return render(request, 'aggregator/query_form.html', {
                'form': form,
                'csv_content': csv_content,
                'headers': reader.fieldnames  # for table headers
            })

    else:
        form = QueryForm()

    return render(request, 'aggregator/query_form.html', {'form': form})
