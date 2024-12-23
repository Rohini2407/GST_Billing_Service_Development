from django import forms
from .models import Business, Invoice, Product

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'gstin']

class InvoiceForm(forms.ModelForm): 

    billing_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']  # Ensure format is YYYY-MM-DD
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']  # Ensure format is YYYY-MM-DD
    )
    class Meta:
        model = Invoice
        fields = ['business','billing_date', 'due_date']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'price_per_unit', 'cgst', 'sgst', 'igst']