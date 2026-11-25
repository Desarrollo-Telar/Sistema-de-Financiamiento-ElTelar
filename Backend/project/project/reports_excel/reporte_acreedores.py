
from openpyxl import Workbook
from django.http import HttpResponse
import json

from django.db.models import Q, Sum
from datetime import datetime, timedelta

# Modelos
from apps.financings.models import PaymentPlan
from apps.accountings.models import Creditor


from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from apps.financings.formato import formatear_numero

def cuota(credito):
    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)
    
    siguiente_pago = PaymentPlan.objects.filter(
        acreedor=credito,
        start_date__lte=dia,
        fecha_limite__gte=dia_mas_uno
    ).first()

    if siguiente_pago is None:
        siguiente_pago = PaymentPlan.objects.filter(
        acreedor=credito).order_by('-id').first()
    
    return siguiente_pago


class ReporteAcreedores(TemplateView):
    def get_queryset(self):
        try:
            request = self.request
            

            # Asignar la consulta a una variable local
            sucursal = self.request.session['sucursal_id']

            query = self.query()
            status = self.status()
            mes = self.query_mes()
            anio = self.query_anio()

            # Crear una lista para almacenar los filtros
            filters = Q()
            excluir = Q()

            
            
            # Añadir filtros si la consulta no está vacía
            if query:
                filters |= Q(fecha_inicio__icontains=query)
                filters |= Q(fecha_vencimiento__icontains=query)           
                filters |= Q(forma_de_pago__icontains=query)
                filters |= Q(codigo_acreedor__icontains=query)



                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(monto__exact=query)
                    filters |= Q(plazo__exact=query)
                    filters |= Q(tasa__exact=query)
            
            if status:
                match status:
                    case 'Recientes':
                        hoy = datetime.now()
                        inicio = hoy - timedelta(days=5)
                        filters &= Q(creation_date__range=[inicio,hoy])

                    case 'Creditos Cancelados':
                        filters &= Q(is_paid_off=True)

                    case 'Creditos en Atraso':
                        filters &= Q(estados_fechas=False)
                        

                    
                    case 'Creditos Falta de Aportacion':
                        filters &= Q(estado_aportacion=False)
                      


                    case 'Creditos con Excedente':
                        filters &= (Q(saldo_actual__lt=0) | Q(excedente__gt=0))
                        
                

            
            
            if anio:
                filters &= Q(creation_date__year=anio)
            
            if mes:
                filters &= Q(creation_date__month=mes)
            
            if sucursal:
                filters &= Q(sucursal=sucursal)

            

            # Filtrar los objetos Banco usando los filtros definidos
            return Creditor.objects.filter(filters).exclude(excluir)
        
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Creditor.objects.none()

    def query(self):
        return self.request.GET.get('q')
    
    def status(self):
        return self.request.GET.get('status')
    
    def query_mes(self):
        return self.request.GET.get('mes')
    
    def query_anio(self):
        return self.request.GET.get('anio')
    
    def get(self, request, *args, **kwargs):
        mes = request.GET.get('mes')
        anio = request.GET.get('anio')
        query = request.GET.get('q')
        status = request.GET.get('status')

        
        
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Reporte de Cartera de Creditos"
        encabezados = [
                "#", "FECHA DE REGISTRO","CODIGO DE ACREEDOR", "NOMBRE DEL ACREEDOR",
                "MONTO OTORGADO","PROPOSITO","PLAZO","TASA","FECHA DE INICIO","FECHA DE VENCIMIENTO","FECHA LIMITE",
                "SALDO ACTUAL","SALDO CAPITAL PENDIENTE","SALDO EXCEDENTE","STATUS POR FECHAS","STATUS POR APORTACION","STATUS CANCELADO",
                "NUMERO DE REFERENCIA"
        ]

        for col_idx, header in enumerate(encabezados, start=1):
            sheet.cell(row=1, column=col_idx, value=header)
        
        # Obtener datos
        informacion_consultada = self.get_queryset()
        contador = 0

        for idx, reporte in enumerate(informacion_consultada, start=2):
            contador += 1
            cuota_limite = cuota(reporte.id)
          
            fecha_limite_pago = cuota_limite.mostrar_fecha_limite().date() if cuota_limite else "---"
           
            numero_referencia = reporte.numero_referencia
            saldo_actual = reporte.saldo_actual
            saldo_capital_pendiente = reporte.saldo_pendiente 
            saldo_excedente = reporte.excedente  
            

            # Mensajes de estado
            if reporte.estado_aportacion:
                mensaje = 'VIGENTE'
            elif reporte.estado_aportacion is None:
                mensaje = 'SIN APORTACIONES'
            else:
                mensaje = 'EN ATRASO'

            aportacion = mensaje
            estado_fechas = 'VIGENTE' if reporte.estados_fechas else 'EN ATRASO'           
            s_credito = 'CANCELADO' if reporte.is_paid_off else 'VIGENTE'


            fila = [
                contador,
                reporte.creation_date.date(),
                reporte.codigo_acreedor,
                reporte.nombre_acreedor if reporte.nombre_acreedor else "Sin Acreedor",
               
                reporte.fmonto(),
                reporte.observaciones,
                reporte.plazo,
                reporte.ftasa(),
                str(reporte.fecha_inicio),
                str(reporte.fecha_vencimiento),            
           
                fecha_limite_pago,
                f"{formatear_numero(saldo_actual)}",
                f"{formatear_numero(saldo_capital_pendiente)}",
                f"{formatear_numero(saldo_excedente)}",

                # Estados
                str(estado_fechas),
                str(aportacion),
                str(s_credito),
                
                f"{numero_referencia}",
            ]

            for col_idx, value in enumerate(fila, start=1):
                sheet.cell(row=idx, column=col_idx, value=value)

        # Crear respuesta de descarga
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        response['Content-Disposition'] = f'attachment; filename="reporte_acreedores_{timestamp}.xlsx"'
        workbook.save(response)
        return response
    