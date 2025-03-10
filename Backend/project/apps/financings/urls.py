# PATH
from django.urls import path, include

# API
from apps.financings.api import routers

# Decorador
from django.contrib.auth.decorators import login_required

# VIEWS
from . import views

app_name = 'financings'

urlpatterns = [
    #------------- CLASIFICACION
    path('clasificar/<str:numero_referencia>/',login_required(views.clasificacion_detallar), name='clasificar'),
    #------------- Boleta
    path('boleta/<str:numero_referencia>/',login_required(views.boleta), name='boleta'),
    # -------------- CREDITO -----------
    path('credit/',login_required(views.list_credit), name='list_credit'),
    path('credit/<int:id>/',login_required(views.detail_credit), name='detail_credit'),
    path('credit/create/',login_required(views.create_credit),name='create_credit'),
    path('credit/search/',login_required(views.CreditSearch.as_view()),name='credit_search'),
    path('credit/estado_cuenta/<int:id>/',login_required(views.detalle_estado_cuenta),name='estado_cuenta'),
    path('credit/estado_cuenta/pdf/<int:id>/',login_required(views.render_pdf_estado_cuenta),name='estado_cuenta_pdf'),
    path('credit/calculos_realizados/pdf/<int:id>/',login_required(views.render_pdf_calculos_credito),name='calculos_realizados'),
    path('credit/plan_pagos/pdf/<int:id>/',login_required(views.render_pdf_plan_pagos),name='plan_pagos'),

    path('contable/acreedor/plan_pagos/pdf/<int:id>/',login_required(views.render_pdf_plan_pagos_acreedor),name='plan_pagos_acreedor'),
    
    path('contable/acreedor/calculos_realizados/pdf/<int:id>/',login_required(views.render_pdf_calculos_credito_acreedor),name='calculos_realizados_acreedor'),
    path('contable/seguro/plan_pagos/pdf/<int:id>/',login_required(views.render_pdf_plan_pagos_seguro),name='plan_pagos_seguro'),
    path('contable/seguro/calculos_realizados/pdf/<int:id>/',login_required(views.render_pdf_calculos_credito_seguro),name='calculos_realizados_seguro'),

    path('credit/delete/<int:id>',login_required(views.delete_credit),name="delete_credit"),
    path('credit/cancelados/',login_required(views.filter_credito_cancelado),name='creditos_cancelados'),
    path('credit/atrasados/',login_required(views.filter_credito_en_atraso),name='creditos_en_atrasos'),
    path('credit/aportacion/',login_required(views.filter_credito_en_falta_aportacion),name='creditos_falta_aportacion'),
    path('credit/reciente/',login_required(views.filter_credito_reciente),name='creditos_recientes'),
    # ---------------- GARANTIA ------------
    path('guarantee/',login_required(views.list_guarantee), name='list_guarantee'),
    path('guarantee/create/',login_required(views.create_guarantee),name='create_guarantee'),
    path('guarantee/detail/<int:id>/',login_required(views.detallar_garantia),name='detallar_garantia'),
    # ---------------- DESEMBOLSO ------------
    path('disbursement/create/<int:id>/',login_required(views.create_disbursement),name='create_disbursement'),  
    path('disbursement/',login_required(views.list_disbursement), name='list_disbursement'),
    path('disbursement/<int:id>/',login_required(views.detallar_desembolso), name='detail_disbursement'),

    # --------------- RECIBO ------------------
    path('recibo/<int:id>/',login_required(views.detallar_recibo), name='recibo'),
    # --------------- FACTURA ------------------
    path('factura/generar/<int:id>/',login_required(views.generar_factura), name='generar_factura'),
    path('factura/<int:id>/',login_required(views.detalle_factura), name='factura'),
    path('factura/pdf/<int:id>/',login_required(views.render_pdf_factura),name='pdf_factura'),
    
    
    # -------------- BOLETAS ---------------------
    path('payment/',login_required(views.list_payment),name='list_payment'),
    path('payment/pendiente/',login_required(views.filter_list_payment_pendiente),name='filter_list_payment_pendiente'),
    path('payment/completado/',login_required(views.filter_list_payment_completados),name='filter_list_payment_completados'),
    path('payment/create/',login_required(views.create_payment),name='create_payment'),
    path('payment/update/<int:id>/',login_required(views.update_pago),name='actualizar_boleta'),
    path('payment/detail/<int:id>/',login_required(views.detalle_boleta),name='detalle_boleta'),
    path('payment/search/',login_required(views.PaymentSearch.as_view()),name='payment_search'),
    path('payment/cuota/update/<int:id>/',login_required(views.update_cuota), name='paymente_update_cuota'),

    # ---------------- BANCOS --------------------
    path('bank/',login_required(views.list_bank),name='list_bank'),
    path('bank/vinculado/',login_required(views.filter_list_bank_vinculado),name='filter_list_bank_vinculado'),
    path('bank/no_viculado/',login_required(views.filter_list_bank_no_vinculado),name='filter_list_bank_no_vinculado'),
    path('bank/search/',login_required(views.BankSearch.as_view()),name='bank_search'),

    # ---------------- REPORTES ----------------
    path('reports/',login_required(views.reportes_generales),name='reportes'),
]

urlpatterns+=routers.urlpatterns