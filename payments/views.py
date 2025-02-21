from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
from django.conf import settings
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from .models import Product  # Import the Product model

# def purchase(request, product_id):
#     products = Product.objects.filter(status='published', availability='available')
#     product = Product.objects.get(id=product_id)
#     paypal_form = PayPalPaymentsForm(initial={
#         'business': "cheche@business.example.com",
#         'amount': product.price,
#         'item_name': product.name,
#         'invoice': product_id,
#         'currency_code': 'USD',
#         'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
#         'return_url': request.build_absolute_uri(reverse('successful')),
#         'cancel_return': request.build_absolute_uri(reverse('cancelled')),
#     })

#     context = {
#         'products': products,  # Send all matching products to the template
#         'paypal_form': paypal_form  # Include the PayPal form in the context
#     }
#     return render(request, 'payments/purchase.html', context)

def purchase(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Use `get_object_or_404` to avoid errors
    products = Product.objects.filter(status='published', availability='available')
    paypal_form = PayPalPaymentsForm(initial={
        'business': "cheche@business.example.com",
        'amount': product.price,
        'item_name': product.name,
        'invoice': str(product.id),  # Ensure invoice is a string
        'currency_code': 'USD',
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(reverse('successful')),
        'cancel_return': request.build_absolute_uri(reverse('cancelled')),
    })

    context = {
        'product': product,  # Pass the specific product
        'products': products,  # Send all matching products to the template
        'paypal_form': paypal_form
    }
    return render(request, 'payments/purchase.html', context)



def detail(request, id):
    product = get_object_or_404(Product, id=id)
    context = {
        'product': product
    }
    return render(request, 'payments/detail.html', context)



def successful(request):
    return render(request, 'payments/successful.html')

def cancelled(request):
    return render(request, 'payments/cancelled.html') 



@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == "Completed":
        try:
            product_id = int(ipn_obj.invoice)  # Get product ID from invoice
            product = Product.objects.get(id=product_id)

            if product.quantity > 0:  # Prevent negative quantity
                product.quantity -= 1
                product.save()
        except Product.DoesNotExist:
            pass  # Handle product not found error gracefully
