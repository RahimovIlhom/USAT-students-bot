from django.urls import path

from .views import BookedTicketsView

urlpatterns = [
    path('booked/', BookedTicketsView.as_view(), name='booked-tickets'),
]
