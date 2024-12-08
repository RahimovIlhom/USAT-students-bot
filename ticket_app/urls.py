from django.urls import path

from .views import BookedTicketsView, PaidTicketsView

urlpatterns = [
    path('booked/', BookedTicketsView.as_view(), name='booked-tickets'),
    path('paid/', PaidTicketsView.as_view(), name='paid-tickets'),
]
