# URL
from django.urls import path, include

# Views
from . import views


# Decorador
from django.contrib.auth.decorators import login_required

app_name = 'dashboard'

urlpatterns = [
    path('clientes_por_mes/', login_required( views.ClientesPorMesAPIView.as_view()), name='clientes_por_mes'),
    path('creditos_por_mes/', login_required(views.CreditosPorMesAPIView.as_view()), name='creditos_por_mes'),
]