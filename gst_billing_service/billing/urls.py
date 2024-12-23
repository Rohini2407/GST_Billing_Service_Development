from django.urls import path
from . import views



urlpatterns = [
    path('create/', views.create_invoice, name='create_invoice'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:invoice_id>/pdf/', views.render_pdf_view, name='render_pdf_view'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
]