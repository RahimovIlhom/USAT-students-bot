from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ticket_app.models import Ticket
from .models import Payment


@login_required(login_url='login')
def confirm_payment(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if ticket.is_booking and ticket.user and ticket.is_paid == False:

        payment, created = Payment.objects.get_or_create(ticket=ticket, amount=ticket.price)

        if request.method == 'GET':
            payment.status = Payment.STATUS_COMPLETED
            payment.paid_at = timezone.now()
            payment.save()

            ticket.is_paid = True
            ticket.save(update_fields=['is_paid'])

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def cancel_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)

    with transaction.atomic():
        payment.status = Payment.STATUS_FAILED
        payment.save()

        payment.ticket.is_paid = False
        payment.ticket.image = None
        payment.ticket.save(update_fields=['is_paid'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
