from django.shortcuts import render, get_object_or_404, redirect

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

# Models
from apps.financings.models import Credit
from apps.InvestmentPlan.models import InvestmentPlan
from apps.subsidiaries.models import Subsidiary

# Formularios
from apps.financings.forms import CreditoForms, PaymentPlanForms
from decimal import Decimal
import json
from django.core.serializers.json import DjangoJSONEncoder
# TIEMPO
from datetime import datetime, date

from .funciones import generar_codigo_seguridad

@login_required
@permiso_requerido('puede_crear_informacion_credito')
def create_credit(request):
    template_name = 'financings/credit/crear_credito.html'
    sucursal = request.session['sucursal_id']

    context = {
        'title':'Creacion de un Credito Nuevo.',
        'sucursal_id':sucursal,
        'permisos':recorrer_los_permisos_usuario(request),
    }

    return render(request,template_name,context)

@login_required
@permiso_requerido('puede_crear_informacion_credito')
def create_credit_aprobado(request, id):
    template_name = 'financings/credit/crear_credito.html'
    sucursal = request.session.get('sucursal_id')
    solicitud = get_object_or_404(InvestmentPlan, id=id)

    if not sucursal and solicitud.sucursal:
        sucursal = solicitud.sucursal.id

    cliente = solicitud.customer_id
    customer_text = f"{cliente.customer_code} - {cliente.first_name} {cliente.last_name}" if cliente else ""

    asesor = solicitud.asesor_responsable
    if not asesor and cliente and hasattr(cliente, 'new_asesor_credito') and cliente.new_asesor_credito:
        asesor = cliente.new_asesor_credito

    advisor_text = f"{asesor.codigo_asesor} - {asesor.nombre} {asesor.apellido}" if asesor else ""
    advisor_id = asesor.id if asesor else ""

    garantias_formateadas = []
    raw_garantias = solicitud.garantias or []
    if isinstance(raw_garantias, list):
        for idx, g in enumerate(raw_garantias):
            if isinstance(g, dict):
                tipo = g.get('tipo') or g.get('tipo_garantia') or 'HIPOTECA'
                try:
                    valor = float(g.get('valor') or g.get('valor_cobertura') or 0)
                except (ValueError, TypeError):
                    valor = 0.0
                specs = g.get('especificaciones') or {}
                if not isinstance(specs, dict):
                    specs = {}

                desc = g.get('descripcion') or ''
                if desc and not any(k in specs for k in ['descripcion', 'Descripcion', 'DescripcionBien']):
                    if tipo == 'MOBILIARIA':
                        specs['DescripcionBien'] = desc
                    elif tipo in ['HIPOTECA', 'DERECHO DE POSESION HIPOTECA']:
                        specs['descripcion'] = desc

                garantias_formateadas.append({
                    'id': int(datetime.now().timestamp() * 1000) + idx,
                    'tipo_garantia': tipo,
                    'valor_cobertura': valor,
                    'especificaciones': specs,
                    'creation_date': datetime.now().isoformat()
                })

    # Si hay fiadores en solicitud.fiador no incluidos como garantía FIADOR
    raw_fiadores = solicitud.fiador or []
    if isinstance(raw_fiadores, list) and raw_fiadores:
        fiador_ids = [f.get('id') for f in raw_fiadores if isinstance(f, dict) and f.get('id')]
        if fiador_ids:
            codigos_existentes = {
                g['especificaciones'].get('Codigo_de_Cliente')
                for g in garantias_formateadas
                if g.get('tipo_garantia') == 'FIADOR' and isinstance(g.get('especificaciones'), dict)
            }
            try:
                from apps.customers.models import Customer
                fiador_customers = Customer.objects.filter(id__in=fiador_ids)
                for f_cust in fiador_customers:
                    if f_cust.customer_code not in codigos_existentes:
                        trabajo = 'N/A'
                        ingreso = 0.0
                        try:
                            from apps.FinancialInformation.models import WorkingInformation
                            info_lab = WorkingInformation.objects.filter(customer_id=f_cust).first()
                            if info_lab:
                                trabajo = info_lab.company_name or info_lab.source_of_income or 'N/A'
                                ingreso = float(info_lab.salary or 0)
                        except Exception:
                            pass

                        garantias_formateadas.append({
                            'id': int(datetime.now().timestamp() * 1000) + len(garantias_formateadas) + 1,
                            'tipo_garantia': 'FIADOR',
                            'valor_cobertura': float(solicitud.total_value_of_the_product_or_service or 0),
                            'especificaciones': {
                                'Codigo_de_Cliente': f_cust.customer_code,
                                'Nombre': f"{f_cust.first_name} {f_cust.last_name}".strip(),
                                'Lugar_de_Trabajo': trabajo,
                                'Ingresos': ingreso,
                                'Numero_de_Telefono': f_cust.telephone or '',
                                'fotografia': str(getattr(f_cust, 'photo', ''))
                            },
                            'creation_date': datetime.now().isoformat()
                        })
            except Exception as e:
                print(f"Error procesando fiadores adicionales: {e}")

    proposito = solicitud.investment_plan_description
    if not proposito:
        proposito = f"Crédito para {solicitud.type_of_product_or_service} correspondiente a Solicitud {solicitud.investment_plan_code}"

    solicitud_dict = {
        'id': solicitud.id,
        'investment_plan_code': solicitud.investment_plan_code,
        'customer_id': cliente.id if cliente else '',
        'customer_text': customer_text,
        'advisor_id': advisor_id,
        'advisor_text': advisor_text,
        'proposito': proposito,
        'monto': float(solicitud.total_value_of_the_product_or_service or 0),
        'tasa_interes': float(solicitud.tasa_interes or 0),
        'plazo': solicitud.plazo or 0,
        'forma_de_pago': solicitud.forma_de_pago or 'NIVELADA',
        'plazo_gracia': solicitud.plazo_gracia or 0,
        'tipo_credito': solicitud.type_of_product_or_service or '',
        'sub_destino': solicitud.sub_destino or proposito or solicitud.type_of_product_or_service or '',
        'fecha_inicio': solicitud.fecha_inicio.strftime('%Y-%m-%d') if solicitud.fecha_inicio else datetime.now().strftime('%Y-%m-%d'),
        'fecha_vencimiento': solicitud.fecha_vencimiento.strftime('%Y-%m-%d') if solicitud.fecha_vencimiento else '',
        'fecha_finalizacion_gracia': solicitud.fecha_finalizacion_gracia.strftime('%Y-%m-%d') if solicitud.fecha_finalizacion_gracia else '',
        'garantias': garantias_formateadas,
    }

    context = {
        'title': 'Creacion de un Credito Nuevo.',
        'sucursal_id': sucursal,
        'solicitud': solicitud,
        'solicitud_data_json': json.dumps(solicitud_dict, cls=DjangoJSONEncoder),
        'permisos': recorrer_los_permisos_usuario(request),
    }

    return render(request, template_name, context)



@login_required
@permiso_requerido('puede_migrar_credito')
def migracion_creditos(request):
    template_name = 'financings/credit/migracion.html'
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'])
    dia = datetime.now()
    mes = dia.month
    anio = dia.year

    form = CreditoForms
    form_cuota = PaymentPlanForms

    num = generar_codigo_seguridad(usuario_regis=request.user, accion='Migración de Credito.')
    request.session['codigo_migracion'] = num
    

   

    if request.method == 'POST':
        form = CreditoForms(request.POST)
        form_cuota = PaymentPlanForms(request.POST)
        
        

        if form.is_valid() and form_cuota.is_valid():
            
            credito = form.save(commit=False)
            cuota = form_cuota.save(commit=False)


            credito.es_credito_migrado = True
            credito.sucursal = sucursal
            credito.estados_fechas = None
            tasa_interes = Decimal(credito.tasa_interes) * Decimal(100)

            if tasa_interes <= 0 :
                credito.tasa_interes = 0.0
                credito.forma_de_pago = 'AMORTIZACIONES A CAPITAL'


            

            
            cuota.outstanding_balance = credito.monto
            cuota.sucursal= sucursal

            nuevo_dia = credito.fecha_inicio.day

            cuota.original_day = nuevo_dia
            try:
                cuota.start_date = date(anio, mes, nuevo_dia)
            except ValueError:
                # Si el día no existe en el mes actual (ej: 31 de febrero),
                # se ajusta al último día del mes actual.
                import calendar
                ultimo_dia = calendar.monthrange(anio, mes)[1]
                cuota.start_date = date(anio, mes, ultimo_dia)

      
            

            credito.save()

            cuota.credit_id = credito

            cuota.save()

            data_credito = model_to_dict(credito)
            data_cuota = model_to_dict(cuota)

            return redirect('financings:detail_credit', credito.id)
        else:
            print(form.errors)
  

    context = {
        'forms': form,
        'forms_cuota':form_cuota,
        'permisos':recorrer_los_permisos_usuario(request),

    }

    return render(request, template_name, context )


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def validar_codigo_seguridad(request):
    # RECUPERAR DE LA SESIÓN, no generar uno nuevo
    codigo_verificar = request.session.get('codigo_migracion')

    if request.method == 'POST':
        data = json.loads(request.body)
        codigo_usuario = data.get('codigo')

        if str(codigo_usuario) == str(codigo_verificar):
            return JsonResponse({'valido': True})
        
        return JsonResponse({'valido': False})
