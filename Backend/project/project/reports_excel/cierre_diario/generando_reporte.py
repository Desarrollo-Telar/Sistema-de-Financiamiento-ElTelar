# Modelos
from apps.actividades.models import InformeDiarioSistema, DetalleInformeDiario

# Reporte Excel
from openpyxl import Workbook
from django.http import HttpResponse
import json


from django.db.models import Q, Sum

# Tiempo
from datetime import datetime

# template
from django.views.generic import TemplateView
from django.http import HttpResponse


# Decoradores
from project.decorador import permiso_requerido
from django.utils.decorators import method_decorator

class CierreDiario(TemplateView):
    
    def get_queryset(self):
        try:
            sucursal = self.request.session['sucursal_id']
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()

            # Añadir filtros si la consulta no está vacía
            if query:
                try:
                    fecha = datetime.strptime(query, '%Y-%m-%d')
                    fecha_inicio = datetime.combine(fecha.date(), datetime.min.time())
                    fecha_fin = datetime.combine(fecha.date(), datetime.max.time())
                    filters |= Q(fecha_registro__range=(fecha_inicio, fecha_fin))
                except ValueError:
                    pass  # No es fecha válida, continúa con los otros filtros


            
            # Filtrar los objetos Customer usando los filtros definidos
            return InformeDiarioSistema.objects.filter(filters, sucursal=sucursal).first()
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return InformeDiarioSistema.objects.all().order_by('-id').first()
        
    def query(self):
        return self.request.GET.get('q')
    
    def get(self, request, *args, **kwargs):
        # Crear el archivo Excel
        dia =  datetime.now().date()
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = f"Reporte de Cierre Diario: {dia}"

        # Encabezados
        encabezados = [
            "#", "Nombre", "Total"
        ]
        for col_idx, header in enumerate(encabezados, start=1):
            sheet.cell(row=1, column=col_idx, value=header)

        # Obtener datos
        informe = self.get_queryset()

        if informe is None:
            return

        registros = DetalleInformeDiario.objects.filter(reporte=informe)

        contador = 0

        for idx, registro in enumerate(registros, start=2):
            contador += 1
            

            fila = [
                contador,
                str(registro.data)
                
            ]

            for col_idx, value in enumerate(fila, start=1):
                sheet.cell(row=idx, column=col_idx, value=value)

        # Crear respuesta de descarga
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        response['Content-Disposition'] = f'attachment; filename="reporte_cierre_diario_{timestamp}.xlsx"'
        workbook.save(response)
        return response

