# URL
from django.urls import path, include

# Views
from . import views


# Decorador
from django.contrib.auth.decorators import login_required

app_name = 'dashboard'

urlpatterns = [
    # General
    path('', login_required(views.dashboard), name='dashboard'),
    # Clientes
    path('clientes-por-mes/', views.ClientesPorMesAPIView.as_view(), name='clientes-por-mes'),
    path('clientes-por-asesor/', views.ClientesPorAsesorMesAPIView.as_view(), name='clientes-por-asesor'),
    
    # Creditos
    path('creditos-por-mes/', views.CreditosPorMesAPIView.as_view(), name='creditos-por-mes'),
    path('tipos-credito/', views.TiposCreditoAPIView.as_view(), name='tipos-credito'),    
    path('formas-pago/', views.FormasPagoAPIView.as_view(), name='formas-pago'),

    path('casos-exito-asesor/', views.CasosExitoAsesorAPIView.as_view(), name='casos-exito-asesor'), # KPI CasosAlDiaAPIView
    path('casos-demanda-asesor/', views.CasosJudicialAsesorAPIView.as_view(), name='casos-demanda-asesor'),
    path('casos-atraso-asesor/', views.CasosAtrasoAsesorAPIView.as_view(), name='casos-atraso-asesor'),
    path('casos-al-dia-asesor/', views.CasosAlDiaAPIView.as_view(), name='casos-al-dia-asesor'),
    path('casos-exito-asesor/power-bi/', views.DetalleCasosExitoAPIView.as_view(), name='casos-exito-asesor-power-bi'), # POWER BI
    path('creditos-por-asesor-mes/', views.CreditosPorAsesorMesAPIView.as_view(), name='creditos-asesor-por-mes'),

    # CONTABLE
    path('desembolsos-por-mes/', views.DesembolsosPorMesAPIView.as_view(), name='desembolsos-por-mes'),
    path('recuperacion-mensual/', views.RecuperacionMensualAPIView.as_view(), name='recuperacion-mensual'),
    path('egresos-por-codigo-mes/', views.EgresosPorCodigoMesAPIView.as_view(),  name='gasto-por-mes'),
    path('bancos-por-mes/', views.BancosPorMesAPIView.as_view(), name='bancos-por-mes'),
    path('acreedores-por-mes/', views.AcreedoresPorMesAPIView.as_view(), name='acreedores-por-mes'),
    path('morosidad-por-mes/', views.MorosidadPorMesAPIView.as_view(), name='morosidad-por-mes'),
]