from django.urls import path

from user_app.views import redirect_admin

urlpatterns = [
    path('', redirect_admin, name='redirect_admin'),
]
