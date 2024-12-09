from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import activate
from django.views import View


def redirect_admin(request):
    return redirect(reverse('dashboard'))


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/dashboard.html')
