from django.urls import path, include
from .import views



urlpatterns = [
    path('purchase/<int:product_id>/', views.purchase, name='purchase'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('successful/', views.successful, name='successful'),
    path('cancelled/', views.cancelled, name='cancelled'),
    path('paypal/', include('paypal.standard.ipn.urls')),
]