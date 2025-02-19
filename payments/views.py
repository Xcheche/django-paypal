from django.shortcuts import render
from .models import Product  # Import the Product model

def purchase(request):
    products = Product.objects.filter(status='published', availability='available')

    context = {
        'products': products  # Send all matching products to the template
    }
    return render(request, 'payments/purchase.html', context)
