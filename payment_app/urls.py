from django.urls import path

from .views import confirm_payment, cancel_payment, PaymentsView

urlpatterns = [
    path('', PaymentsView.as_view(), name='payments'),
    path('cancel/<int:payment_id>/', cancel_payment, name='cancel_payment'),
    path('confirm/<int:ticket_id>/', confirm_payment, name='confirm_payment'),
]
