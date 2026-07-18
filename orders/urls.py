from django.urls import path
from . import views
from .invoice import download_invoice

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('track/', views.TrackOrderView.as_view(), name='track_order'),
    path('history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('verify/', views.VerifyPaymentView.as_view(), name='verify_payment'),
    path('invoice/<int:order_id>/', download_invoice, name='download_invoice'),
]