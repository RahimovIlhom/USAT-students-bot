from audioop import reverse

from django.shortcuts import redirect
from django.urls import reverse_lazy


def redirect_admin(request):
    return redirect('/uz/admin')
