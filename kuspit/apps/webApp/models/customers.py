from django.db import models
from compartidos.models import TimestampedModel


# Create customers model from TimestampedModel
class Customer(TimestampedModel):
    name = models.CharField(max_length=50)
    paternal_surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class PaymentsCustomer(TimestampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField()                                        # TODO: Check if amount is meant to be price
    product_name = models.CharField(max_length=50)
    quantity = models.IntegerField()

    def __str__(self):
        return self.customer.name
