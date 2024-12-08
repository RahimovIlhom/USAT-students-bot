from django.urls import path

from .views import confirm_payment, cancel_payment

urlpatterns = [
    path('cancel/<int:payment_id>/', cancel_payment, name='cancel_payment'),
    path('confirm/<int:ticket_id>/', confirm_payment, name='confirm_payment'),
]
