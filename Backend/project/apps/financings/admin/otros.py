# ADMIN
from django.contrib import admin

# MODELO
from apps.financings.models import Guarantees, DetailsGuarantees, Invoice, Cuota




GARANTIA = admin.site.register(Guarantees)
DETALLE_DE_GARANTIA = admin.site.register(DetailsGuarantees)
FACTURA = admin.site.register(Invoice)
CUOTA = admin.site.register(Cuota)