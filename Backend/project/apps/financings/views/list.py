from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo
from apps.customers.models import Customer
from apps.financings.models import Invoice


from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

from datetime import datetime,timedelta
# Obtener la fecha y hora actual
now = datetime.now()
# CLASES
from apps.financings.clases.paymentplan import PaymentPlan as PlanPagoos
from apps.financings.clases.credit import Credit as Credito

# TAREA ASINCRONICO
from apps.financings.task import cambiar_plan

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q


@login_required
@usuario_activo
def list_factura(request):
    pass