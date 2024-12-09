from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_GET

from ticket_app.models import Ticket
from .tasks import generate_ticket_image, cancel_payment_error_msg
from .models import Payment


@login_required(login_url='login')
@require_GET
def confirm_payment(request, ticket_id):
    # Chiptani olish
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    # Chiptaning to'lov holatini tekshirish
    if ticket.is_booking and ticket.user and not ticket.is_paid:
        with transaction.atomic():
            # To'lovni olish yoki yaratish
            payment, created = Payment.objects.get_or_create(
                user=ticket.user,
                ticket=ticket,
                defaults={'amount': ticket.price}
            )

            # To'lovni tasdiqlash
            payment.status = Payment.STATUS_COMPLETED
            payment.paid_at = timezone.now()
            payment.save(update_fields=['status', 'paid_at'])

            # Chiptani yangilash
            ticket.is_paid = True
            ticket.save(update_fields=['is_paid'])

            # Chiptani yaratishni fon vazifasiga qo'shish
            generate_ticket_image.delay(ticket.user.tg_id, ticket.event.id, ticket.user.student.fullname, ticket.id)

    # Avvalgi sahifaga qaytarish
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required(login_url='login')
@require_GET
def cancel_payment(request, payment_id):
    # To'lov ma'lumotlarini olish
    payment = get_object_or_404(Payment, pk=payment_id)

    # Atomar tranzaksiyada statusni yangilash
    with transaction.atomic():
        payment.status = Payment.STATUS_FAILED
        payment.save(update_fields=['status'])

        payment.ticket.is_paid = False
        payment.ticket.image = None
        payment.ticket.save(update_fields=['is_paid', 'image'])

        cancel_payment_error_msg.delay(payment.ticket.user.tg_id, payment.ticket.id)

    # Avvalgi sahifaga qaytarish
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


class PaymentsView(LoginRequiredMixin, View):
    def get(self, request):
        payments = Payment.objects.filter().order_by('-created_at')

        context = {
            'payments': payments
        }
        return render(request, context=context, template_name='payments/payments.html')
