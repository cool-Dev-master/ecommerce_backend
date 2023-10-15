from django.contrib.auth.models import User
from django.db import models
# from django.contrib.postgres.fields import JSONField
# from django.utils import timezone

def default_data():
    return {'quantity': 0, 'active':False, 'orders':[]}

class Customer(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, default=None)
    cart = models.JSONField(default=default_data)
    isActive = models.BooleanField(default=True, blank=True)
    isDeleted = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.user.username

# class Customer(models.Model):
#     id = models.BigAutoField(primary_key=True, unique=True, auto_created=True)
#     name = models.CharField(max_length=30)
#     phoneNumber = models.IntegerField()
#     email = models.EmailField(max_length=100, blank=True, default=None)
#     password = models.CharField(max_length=8)
#     isActive = models.BooleanField(default=True)
#     created_at = models.DateTimeField(default=timezone.now)
#     # created_at = models.DateTimeField(auto_now_add=True, default=)
#     isDeleted = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name

    