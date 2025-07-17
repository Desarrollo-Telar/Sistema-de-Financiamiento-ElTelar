# VISTAS
from apps.financings.views import *

# PATH
from django.urls import path, include

# DECORADOR
from django.contrib.auth.decorators import login_required

urlpatterns_recibo = [
    # --------------- RECIBO ------------------
    path('recibo/<int:id>/',login_required(detallar_recibo), name='recibo'),
    path('recibo/pdf/<int:id>/',login_required(render_pdf_recibo), name='recibo_pdf'),
    path('recibo/', login_required(RecibosListView.as_view()), name='recibos'),
    # --------------- FACTURA ------------------
    path('factura/generar/<int:id>/',login_required(generar_factura), name='generar_factura'),
    path('factura/<int:id>/',login_required(detalle_factura), name='factura'),
    path('factura/pdf/<int:id>/',login_required(render_pdf_factura),name='pdf_factura'),
]