from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


# Custom Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        # Foydalanuvchi nomi va parolni olish
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Foydalanuvchi ma'lumotlarini tekshirish
        user = authenticate(request, username=username, password=password)

        if user is not None:  # To'g'ri foydalanuvchi
            login(request, user)  # Login
            messages.success(request, _('Siz muvaffaqiyatli kirishingiz'))
            return redirect('dashboard')
        else:
            messages.error(request, _('Foydalanuvchi nomi yoki parol noto‘g‘ri'))

    return render(request, 'accounts/login.html')


# Custom Logout View
@login_required(login_url='login')
def logout_view(request):
    logout(request)  # Logout
    messages.info(request, _("Siz muvaffaqiyatli chiqdingiz"))
    return redirect('login')
