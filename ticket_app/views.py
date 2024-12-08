from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .models import Ticket


class BookedTicketsView(LoginRequiredMixin, View):
    def get(self, request):
        booked_tickets = Ticket.objects.filter(is_paid=False, is_booking=True, booking_at__isnull=False).order_by('-booking_at')

        context = {
            'booked_tickets': booked_tickets
        }
        return render(request, context=context, template_name='tickets/booked_tickets.html')


class PaidTicketsView(LoginRequiredMixin, View):
    def get(self, request):
        paid_tickets = Ticket.objects.filter(is_paid=True).order_by('-booking_at')

        context = {
            'paid_tickets': paid_tickets
        }
        return render(request, context=context, template_name='tickets/paid_tickets.html')
