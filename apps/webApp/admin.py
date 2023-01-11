# Librerías de Terceros
from django.contrib import admin

# Proyecto
from .models import FrequentQuestions, PaymentsCustomer, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "email", "name", "paternal_surname"]


@admin.register(PaymentsCustomer)
class PaymentsCustomerAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "customer", "amount", "product_name", "quantity"]


@admin.register(FrequentQuestions)
class FrequentQuestionsAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = [
        "id",
        "question",
        "answer",
        "is_active",
    ]
