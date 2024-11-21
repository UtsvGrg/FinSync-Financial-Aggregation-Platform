from django import forms

# Define choices for the dropdown menu
OPERATOR_CHOICES = [
    ('', ''),
    ('<', '<'),
    ('>', '>'),
    ('>=', '>='),
    ('<=', '<='),
]

class QueryForm2(forms.Form):
    llm_search = forms.CharField(label='LLM Query', max_length=100, required=False)
    
class QueryForm(forms.Form):
    # Fields with their respective dropdown for operators
    revenue_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Revenue')
    revenue = forms.IntegerField(label='', required=False)
    
    operating_expenses_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Operating Expenses')
    operating_expenses = forms.IntegerField(label='', required=False)
    
    long_term_assets_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Long-term Assets')
    long_term_assets = forms.IntegerField(label='', required=False)
    
    amortization_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Amortization')
    amortization = forms.IntegerField(label='', required=False)
    
    cash_raised_spent_on_debt_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Cash Raised/Spent on Debt')
    cash_raised_spent_on_debt = forms.IntegerField(label='', required=False)
    
    taxes_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Taxes')
    taxes = forms.IntegerField(label='', required=False)
    
    net_income_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Net Income')
    net_income = forms.IntegerField(label='', required=False)
    
    ending_cash_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Ending Cash')
    ending_cash = forms.IntegerField(label='', required=False)
    
    cash_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Cash')
    cash = forms.IntegerField(label='', required=False)
    
    current_liabilities_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Current Liabilities')
    current_liabilities = forms.IntegerField(label='', required=False)
    
    cash_raised_spent_on_equity_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Cash Raised/Spent on Equity')
    cash_raised_spent_on_equity = forms.IntegerField(label='', required=False)
    
    non_cash_items_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Non-Cash Items')
    non_cash_items = forms.IntegerField(label='', required=False)
