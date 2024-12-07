from django.urls import path

from .views import redirect_admin, DashboardView

urlpatterns = [
    path('', redirect_admin, name='redirect_admin'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
