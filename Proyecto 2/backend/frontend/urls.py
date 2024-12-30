from django.urls import path
from .views import login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', login_view, name='home'),  # Redirige la URL de inicio a la vista de login
]
