from django.shortcuts import render, get_object_or_404, redirect
from .models import Business, Invoice, Product
from .forms import BusinessForm, InvoiceForm, ProductForm
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.contrib import messages
from decimal import Decimal


# Helper Function to Generate Invoice Numbers
def generate_invoice_number():
    last_invoice = Invoice.objects.order_by('id').last()
    if last_invoice:
        return f"INV-{last_invoice.id + 1:04d}"
    return "INV-0001"

# Create Invoice View

def create_invoice(request):
    ProductFormSet = inlineformset_factory(Invoice, Product, form=ProductForm, extra=1)
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        formset = ProductFormSet(request.POST)
        
        # Debug: Log incoming POST data
        print("POST Data:", request.POST)

        # Check form validation
        if not invoice_form.is_valid():
            print("Invoice Form Errors:", invoice_form.errors)
        if not formset.is_valid():
            print("Formset Errors:", formset.errors)

        if invoice_form.is_valid() and formset.is_valid():
            invoice = invoice_form.save(commit=False)
            invoice.invoice_number = generate_invoice_number()
            invoice.total_amount = 0  # Initialize total amount
            invoice.save()

            total_amount = 0
            formset.instance = invoice  # Set the instance for the formset
            for form in formset:
                product = form.save(commit=False)
                total_price = product.quantity * product.price_per_unit
                product.cgst = total_price * Decimal('0.09')  # 9% CGST
                product.sgst = total_price * Decimal('0.09')  # 9% SGST
                product.igst = total_price * Decimal('0.18')  # 18% IGST
                product.invoice = invoice
                product.save()
                total_amount += total_price + product.cgst + product.sgst + product.igst
            invoice.total_amount = total_amount
            invoice.save()

            formset.save()
            print(f"Invoice {invoice.id} successfully created. Redirecting to details page.")
            return redirect('invoice_detail', invoice_id=invoice.id)

        else:
            messages.error(request, "There were errors in the form. Please check and try again.")

    else:
        invoice_form = InvoiceForm()
        formset = ProductFormSet()
    
    return render(request, 'billing/create_invoice.html', {
        'invoice_form': invoice_form,
        'formset': formset,
    })

# Invoice Detail View
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})

# Generate PDF View
def render_pdf_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    html = render_to_string('billing/pdf_template.html', {'invoice': invoice})
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response

# CRUD for Products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'billing/product_list.html', {'products': products})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'billing/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'billing/product_confirm_delete.html', {'product': product})
