# VISTAS
from apps.financings.views import *

# PATH
from django.urls import path, include

# DECORADOR
from django.contrib.auth.decorators import login_required

urlpatterns_credit = [
    # -------------- CREDITO -----------
    path('credit/',login_required(list_credit), name='list_credit'),
    path('credit/<int:id>/',login_required(detail_credit), name='detail_credit'),
    path('credit/create/',login_required(create_credit),name='create_credit'),
    path('credit/delete/<int:id>',login_required(delete_credit),name="delete_credit"),
    path('credit/search/',login_required(CreditSearch.as_view()),name='credit_search'),
    path('credit/estado_cuenta/<int:id>/',login_required(detalle_estado_cuenta),name='estado_cuenta'),
    path('credit/estado_cuenta/pdf/<int:id>/',login_required(render_pdf_estado_cuenta),name='estado_cuenta_pdf'),
    path('credit/calculos_realizados/pdf/<int:id>/',login_required(render_pdf_calculos_credito),name='calculos_realizados'),
    path('credit/plan_pagos/pdf/<int:id>/',login_required(render_pdf_plan_pagos),name='plan_pagos'),
    path('credit/clasificar/',list_clasificacion, name='list_clasificacion'),
    path('credit/excedente/',filter_credito_con_excedente, name='filter_credito_con_excedente'),
    path('credit/clasificacion_mes_anio/',filter_credito_por_mes_anio, name='filter_credito_por_mes_anio'),
    
    path('credit/cancelados/',login_required(filter_credito_cancelado),name='creditos_cancelados'),
    path('credit/atrasados/',login_required(filter_credito_en_atraso),name='creditos_en_atrasos'),
    path('credit/aportacion/',login_required(filter_credito_en_falta_aportacion),name='creditos_falta_aportacion'),
    path('credit/reciente/',login_required(filter_credito_reciente),name='creditos_recientes'),
    path('credit/reciente/x',login_required(filter_credito_con_aportaciones),name='filter_credito_con_aportaciones'),
    path('credit/fecha_vencimiento/',login_required(filter_credito_fecha_vencimiento_hoy),name='filter_credito_fecha_vencimiento_hoy'),
    path('credit/fecha_limite/',login_required(filter_credito_fecha_limite_hoy),name='filter_credito_fecha_limite_hoy'),
    path('credit/proximos/fecha_vencimiento/',login_required(filter_credito_proximos_vencerse),name='filter_credito_proximos_vencerse'),

    

]