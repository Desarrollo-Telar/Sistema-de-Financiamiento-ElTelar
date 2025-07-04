# PATH
from django.urls import path, include

# API
from apps.financings.api import routers

# Decorador
from django.contrib.auth.decorators import login_required

# VIEWS
from . import views

# RUTAS
from .rutas import *

app_name = 'financings'

urlpatterns = [
    #------------- CLASIFICACION
    path('clasificar/<str:numero_referencia>/',login_required(views.clasificacion_detallar), name='clasificar'),

    #------------- FUNCIONES
    path('status/boletas/',login_required(views.async_view_boletas),name='comparacion_boletas'),
    path('status/banco/',login_required(views.async_view_banco),name='comparacion_bancos'),
    path('boleta/<str:numero_referencia>/',login_required(views.boleta), name='boleta'),
    

    # ---------------- RUTAS NO VAN AQUI ------------------------------
    path('contable/acreedor/plan_pagos/pdf/<int:id>/',login_required(views.render_pdf_plan_pagos_acreedor),name='plan_pagos_acreedor'),
    path('contable/acreedor/calculos_realizados/pdf/<int:id>/',login_required(views.render_pdf_calculos_credito_acreedor),name='calculos_realizados_acreedor'),
    path('contable/seguro/plan_pagos/pdf/<int:id>/',login_required(views.render_pdf_plan_pagos_seguro),name='plan_pagos_seguro'),
    path('contable/seguro/calculos_realizados/pdf/<int:id>/',login_required(views.render_pdf_calculos_credito_seguro),name='calculos_realizados_seguro'),

    # ---------------- REPORTES ----------------
    path('reports/',login_required(views.reportes_generales),name='reportes'),
    
]

urlpatterns+=routers.urlpatterns + urlpatterns_bank + urlpatterns_credit + urlpatterns_disbursement + urlpatterns_guarantee + urlpatterns_payment + urlpatterns_recibo