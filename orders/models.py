from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from customers.models import Customer
from products.models import Product

# Create your models here.

class Order(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    order_date = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False, blank=True)
    isActive = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.id
