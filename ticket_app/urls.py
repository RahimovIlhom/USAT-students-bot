from django.urls import path

from .views import BookedTicketsView, AllTicketsView

urlpatterns = [
    path('all/', AllTicketsView.as_view(), name='all-tickets'),
    path('booked/', BookedTicketsView.as_view(), name='booked-tickets'),
]
