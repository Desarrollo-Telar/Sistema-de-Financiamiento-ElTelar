# URL
from django.urls import path, include

# vistas
from apps.customers import views

# Decorador
from django.contrib.auth.decorators import login_required


urlpatterns_asesores_creditos = [
    path('asesores_credito/',login_required( views.AsesoresCreditosList.as_view()), name='asesores_creditos'),
    path('asesores_credito/detail/<str:codigo_asesor>/',login_required( views.detail_asesor), name='detail_asesor'),
    path('asesores_credito/cobranza/',login_required( views.CobranzaList.as_view()), name='cobranza_asesor'),
    path('asesores_credito/cobranza/crear/',login_required( views.creacion_cobranza), name='creacion_cobranza'),
    path('asesores_credito/cobranza/actualizar/<int:id>/',login_required( views.actualizacion_cobranza), name='actualizacion_cobranza'),
    path('asesores_credito/cobranza/eliminar/<int:id>/',login_required( views.eliminacion_cobranza), name='eliminacion_cobranza'),
    path('asesores_credito/cobranza/informe/<str:user_code>/<int:id>/',login_required( views.detail_informe), name='detail_informe_cobranza'),

]