# PATH
from django.urls import path, include

# API
from apps.InvestmentPlan.api import routers

# Decorador
from django.contrib.auth.decorators import login_required

# VIEWS
from . import views, generate_pdf


app_name = 'investment_plan'

urlpatterns = [
    path('create/<str:customer_code>/',views.create_plan_financiamiento, name='create' ),
    path('delete/<int:id>/<str:customer_code>/',views.delete_plan_financiamiento,name='delete'),
    path('update/<int:id>/<str:customer_code>/',views.update_plan_financiamiento, name='update'),
    path('pagare/<int:id>/<str:customer_code>/',generate_pdf.render_pagare_docx, name='pagare'),
    path('plan_pagos/<int:id>/<str:customer_code>/',generate_pdf.render_plan_pagos_docx, name='plan_pagos'),
    path('gestion_de_expedientes_notarios/<int:id>/',views.gestion_de_expedientes_notarios, name='gestion_de_expedientes_notarios'),
    path('subir_archivos/<int:plan_id>/<int:user_id>/',views.subir_archivos_expedientes_notarios, name='subir_archivos'),
    path('lista_expedientes_notarios/<uuid:uuid>/',views.lista_expedientes_notarios, name='lista_expedientes_notarios'),

]

urlpatterns += routers.urlpatterns