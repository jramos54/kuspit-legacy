from django.contrib import admin
from .models import Customer, PaymentsCustomer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "email", "name", "paternal_surname"]


@admin.register(PaymentsCustomer)
class PaymentsCustomerAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "customer", "amount", "product_name", "quantity"]

