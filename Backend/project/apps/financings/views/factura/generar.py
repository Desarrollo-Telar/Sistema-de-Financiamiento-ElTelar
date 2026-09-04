import requests  # Importación necesaria para capturar RequestException
from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Payment, PaymentPlan, AccountStatement, Recibo
from apps.financings.models import Invoice, Credit

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from scripts.INFILE.fact import guardar_xml_recibo
from scripts.INFILE.consulta_nit import consulta_receptor

# FORMULARIO
from apps.financings.forms import PaymentPlanForms, BoletaForm

# Manejo de mensajes
from django.contrib import messages

@login_required
@usuario_activo
def generar_factura(request, id):
    recibo = get_object_or_404(Recibo, id=id)
    factura_data = model_to_dict(recibo)
    
    # Si ya tiene factura, no volver a certificar
    if recibo.factura:
        messages.info(request, "Este recibo ya fue facturado.")
        return redirect('financings:factura_list', recibo.pago.credit.id)
    
    if recibo.cliente is None:
        messages.error(request, "NO SE PUEDE FACTURAR, EL RECIBO NO PERTENECE A UN CLIENTE")
        return redirect('index')

    try:
        if not consulta_receptor(recibo.cliente.number_nit):
            messages.error(request, "NIT NO VÁLIDO")
            return redirect('index')

        # Generar y enviar XML a FEL
        # Asegúrate de que guardar_xml_recibo registre o cree la Invoice en BD si no existía
        ruta_guardado = guardar_xml_recibo(
            recibo, 
            nombre_archivo=f"recibo_{recibo.id}_{recibo.fecha.strftime('%Y%m%d')}.xml"
        )
        print("Archivo XML guardado en:", ruta_guardado)

        # Buscar la instancia creada/actualizada
        factura_instance = Invoice.objects.filter(recibo_id=recibo).first()
        
        # Validación de seguridad: verificar que realmente se obtuvo la instancia
        if not factura_instance or not factura_instance.numero_autorizacion:
            log_system_event('Error al recuperar factura generada', "ERROR", 'Sistema', 'Facturación', 'No se encontró la factura en BD o no posee UUID', factura_data)
            messages.error(request, "El documento fue procesado pero no se pudo obtener el número de autorización (UUID).")
            return redirect('financings:factura_list', recibo.pago.credit.id)

        log_system_event('Factura generada y certificada exitosamente.', "INFO", 'Sistema', 'Facturación', None, None)
        messages.success(request, "Factura generada y certificada exitosamente.")
        
        return redirect(f"https://report.feel.com.gt/ingfacereport/ingfacereport_documento?uuid={factura_instance.numero_autorizacion}")

    except ValueError as e:
        log_system_event('Error de configuración', "ERROR", 'Sistema', 'Facturación', f'{e}', factura_data)
        messages.error(request, f"Error de configuración: {e}")

    except requests.exceptions.RequestException as e:  # Corregido: requests (librería) en lugar de request (vista)
        log_system_event('Error de conexión con la API FEL', "ERROR", 'Sistema', 'Facturación', f'{e}', factura_data)
        messages.error(request, "No se pudo conectar con el servicio de certificación FEL.")

    except Exception as e:
        log_system_event('Error al generar factura para el recibo', "ERROR", 'Sistema', 'Facturación', f'{e}', factura_data)
        messages.error(request, f"Ocurrió un error al generar la factura: {e}")

    return redirect('financings:factura_list', recibo.pago.credit.id)