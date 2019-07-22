from django import forms


class StockForm(forms.Form):
    stock_name = forms.CharField(label='stock_name', max_length=20)
    stock_code = forms.CharField(label='stock_code', max_length=20)
    industry_code = forms.CharField(label='industry_code', max_length=20)