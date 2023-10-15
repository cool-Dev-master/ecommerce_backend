from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key= True, auto_created=True)
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='product', null=True, default= None, blank=True)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=500, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name