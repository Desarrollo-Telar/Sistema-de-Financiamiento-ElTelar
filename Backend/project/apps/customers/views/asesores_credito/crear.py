from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.customers.models import Customer, CreditCounselor, Cobranza
from apps.actividades.models import Informe, DetalleInformeCobranza
from apps.financings.models import PaymentPlan, Credit
from django.db.models import Q

# Formulario
from apps.customers.forms import CobranzaForms

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido

# MENSAJES
from django.contrib import messages

# Tiempo
from datetime import datetime,timedelta, date

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from scripts.recoleccion_informacion.detalle_asesor_credito import recoleccion_informacion_detalle_asesor


def obtener_cuota(credito):
    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)

    siguiente_pago = PaymentPlan.objects.filter(
        credit_id=credito,
        start_date__lte=dia,
        fecha_limite__gte=dia_mas_uno
    ).first()

    if siguiente_pago is None:
        siguiente_pago = PaymentPlan.objects.filter(credit_id=credito).order_by('-id').first()
    
    return siguiente_pago

def obtener_informe_asesor(credito, asesor_autenticado):
    if credito.asesor_de_credito != asesor_autenticado:
        informe_reporte = Informe.objects.filter(
            usuario=credito.customer_id.new_asesor_credito.usuario,
            esta_activo=True
        ).first()

        if informe_reporte is None:
            informe_reporte = Informe.objects.create(
                usuario=credito.asesor_de_credito.usuario,
                esta_activo=True,
                nombre_reporte=f'INVERSIONES INTEGRALES EL TELAR'
            )
        
        return informe_reporte

def registrar_cobranza_detalle_existente(detalle_existente, fcobranza, asesor_autenticado, info_cuota, form):
    # Ya existe -> actualizamos la cobranza existente
    cobranza_existente = detalle_existente.cobranza
    fecha = form.cleaned_data.get('fecha_promesa_pago')
    fecha_gestion = form.cleaned_data.get('fecha_gestion')

    if fecha is None:
        fecha = date.today()
            
    if fecha_gestion is None:
        fcobranza.fecha_gestion = date.today()

    resultado = form.cleaned_data.get('resultado')

    if resultado != 'Promesa de pago':
        fcobranza.fecha_seguimiento = fecha
        fcobranza.fecha_promesa_pago = None
    else:
        fcobranza.fecha_seguimiento = None
        fcobranza.fecha_promesa_pago = fecha
    
    # Actualizamos los campos que vienen del formulario
    cobranza_existente.tipo_cobranza = fcobranza.tipo_cobranza
    cobranza_existente.fecha_gestion = fcobranza.fecha_gestion
    cobranza_existente.tipo_gestion = fcobranza.tipo_gestion
    cobranza_existente.resultado = fcobranza.resultado
    cobranza_existente.fecha_promesa_pago = fcobranza.fecha_promesa_pago
    cobranza_existente.observaciones = fcobranza.observaciones
    cobranza_existente.estado_cobranza = fcobranza.estado_cobranza
    cobranza_existente.mora_pendiente = fcobranza.mora_pendiente
    cobranza_existente.interes_pendiente = fcobranza.interes_pendiente
    cobranza_existente.monto_pendiente = fcobranza.monto_pendiente
    cobranza_existente.telefono_contacto = fcobranza.telefono_contacto
    cobranza_existente.fecha_seguimiento = fcobranza.fecha_seguimiento
    cobranza_existente.fecha_limite_cuota = info_cuota.mostrar_fecha_limite().date()
    cobranza_existente.cuota = info_cuota
    cobranza_existente.asesor_credito = asesor_autenticado
    cobranza_existente.save()
    return cobranza_existente


@login_required
@permiso_requerido('puede_crear_registro_cobranza')
def creacion_cobranza(request):
    template_name = 'cobranza/create.html'

    credito_q = Credit.objects.filter(id=request.GET.get('q')).first()

    
    informe_usuario = Informe.objects.filter(
        usuario=request.user,
        esta_activo=True
    ).first() # ESTE INFORME ES PARA LA PERSONA QUE VA A REALIZAR DICHO REGISTRO

    if informe_usuario is None:
        informe_usuario = Informe.objects.create(
            usuario=request.user,
            esta_activo=True,
            nombre_reporte=f'INVERSIONES INTEGRALES EL TELAR'
        )

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    
    
   
    
    if asesor_autenticado is None:
        return redirect('index')
    
   

    if request.method == 'POST':
        form = CobranzaForms(request.POST)

        if form.is_valid():
            fcobranza = form.save(commit=False) # SE PAUSA EL REGISTRO

            
            
            # OBTENER INFORMACION DEL CREDITO DE ESTA COBRANZA
            if credito_q is not None:
                credito = credito_q
            else:
                credito = Credit.objects.filter(id=fcobranza.credito.id).first()

            # PARA OBTENER LA CUOTA ACTUAL
            info_cuota = obtener_cuota(credito)
            
            informe_reporte = obtener_informe_asesor(credito, asesor_autenticado)

            detalle_existente = DetalleInformeCobranza.objects.filter(reporte=informe_reporte,cobranza__credito=credito).first() # POR SI VIENEN DE LA VISTA DETALLE DEL CREDITO

            detalle_info_e =  DetalleInformeCobranza.objects.filter(reporte=informe_usuario,cobranza__credito=credito).first()
            cobranza = None

            if detalle_existente:
                cobranza = registrar_cobranza_detalle_existente(detalle_existente, fcobranza, asesor_autenticado, info_cuota, form)
            else:
                fecha = form.cleaned_data.get('fecha_promesa_pago')
                fecha_gestion = form.cleaned_data.get('fecha_gestion')

                if fecha is None:
                    fecha = date.today()
                
                if fecha_gestion is None:
                    fcobranza.fecha_gestion = date.today()

                resultado = form.cleaned_data.get('resultado')

                if resultado != 'Promesa de pago':
                    fcobranza.fecha_seguimiento = fecha
                    fcobranza.fecha_promesa_pago = None
                else:
                    fcobranza.fecha_seguimiento = None
                    fcobranza.fecha_promesa_pago = fecha


                fcobranza.fecha_limite_cuota = info_cuota.mostrar_fecha_limite().date()
                fcobranza.cuota = info_cuota
                fcobranza.asesor_credito = asesor_autenticado
                fcobranza.save()
                cobranza = fcobranza

                DetalleInformeCobranza.objects.create(
                    reporte = informe_reporte,
                    cobranza = cobranza
                )

            if detalle_info_e:
                detalle_info_e.cobranza = cobranza
                detalle_info_e.save()

            else:
                DetalleInformeCobranza.objects.create(
                    reporte = informe_usuario,
                    cobranza = cobranza
                )



            
            


            messages.success(request, "Registro Completado Con Exito.")
            return redirect('customers:cobranza_asesor')
    else:
        form = CobranzaForms()
        if credito_q is not None:
            form = CobranzaForms(initial={'credito': credito_q})
        
        

            

    context = {
        'title': f'Registro de Cobranza | {asesor_autenticado} |',
        'form': form,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

