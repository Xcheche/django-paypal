from django.db import models

# Create your models here.

class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    availability = models.CharField(max_length=15, choices=AVAILABILITY_CHOICES, default='available')
    name = models.CharField(max_length=255)
   
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', default='products/no-image.jpg')

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
  

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
