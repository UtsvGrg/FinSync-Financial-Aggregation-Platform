from django import forms

# Define choices for the dropdown menu
OPERATOR_CHOICES = [
    ('', ''),
    ('<', '<'),
    ('>', '>'),
    ('>=', '>='),
    ('<=', '<='),
]

class QueryForm(forms.Form):
    # Fields with their respective dropdown for operators
    revenue_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Revenue')
    revenue = forms.CharField(label='', max_length=100, required=False)
    
    operating_expenses_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Operating Expenses')
    operating_expenses = forms.CharField(label='', max_length=100, required=False)
    
    long_term_assets_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Long-term Assets')
    long_term_assets = forms.CharField(label='', max_length=100, required=False)
    
    amortization_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Amortization')
    amortization = forms.CharField(label='', max_length=100, required=False)
    
    cash_raised_spent_on_debt_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Cash Raised/Spent on Debt')
    cash_raised_spent_on_debt = forms.CharField(label='', max_length=100, required=False)
    
    taxes_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Taxes')
    taxes = forms.CharField(label='', max_length=100, required=False)
    
    net_income_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Net Income')
    net_income = forms.CharField(label='', max_length=100, required=False)
    
    ending_cash_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Ending Cash')
    ending_cash = forms.CharField(label='', max_length=100, required=False)
    
    cash_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Cash')
    cash = forms.CharField(label='', max_length=100, required=False)
    
    current_liabilities_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Current Liabilities')
    current_liabilities = forms.CharField(label='', max_length=100, required=False)
    
    cash_raised_spent_on_equity_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Cash Raised/Spent on Equity')
    cash_raised_spent_on_equity = forms.CharField(label='', max_length=100, required=False)
    
    non_cash_items_operator = forms.ChoiceField(choices=OPERATOR_CHOICES, required=False, label='Non-Cash Items')
    non_cash_items = forms.CharField(label='', max_length=100, required=False)
