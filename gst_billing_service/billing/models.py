from django.db import models

class Business(models.Model):
    name = models.CharField(max_length=255)
    gstin = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    business = models.CharField(max_length=100) 
    invoice_number = models.CharField(max_length=20, unique=True)
    billing_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.invoice_number

class Product(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    cgst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    sgst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    igst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def total_price(self):
        return self.quantity * self.price_per_unit

    def __str__(self):
        return self.name

