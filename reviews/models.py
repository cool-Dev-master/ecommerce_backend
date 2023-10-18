from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from customers.models import Customer
from products.models import Product

# Create your models here.
class Review(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    review = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    reviewed_date = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return str(self.id)

