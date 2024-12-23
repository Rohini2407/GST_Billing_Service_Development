import re
from django import forms
from .models import Business, Invoice, Product

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'gstin']

def clean_gstin(self):
        gstin = self.cleaned_data.get('gstin')
        if not re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$', gstin):
            raise forms.ValidationError("Invalid GSTIN format. Ensure it is a 15-character alphanumeric value.")
        return gstin

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
        fields = ['business','gstin','billing_date', 'due_date']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'price_per_unit', 'cgst', 'sgst', 'igst']