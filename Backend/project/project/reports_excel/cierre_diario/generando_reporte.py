# Modelos
from apps.actividades.models import InformeDiarioSistema, DetalleInformeDiario

# Reporte Excel
from openpyxl import Workbook
from django.http import HttpResponse
import json
import io
import zipfile


from django.db.models import Q, Sum
# Funciones
from .cierre_clientes import crear_excel_clientes
from .cierre_creditos import crear_excel_creditos
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
        


        zip_buffer = io.BytesIO()
        zip_file = zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED)

        # Obtener datos
        informe = self.get_queryset()
        dia =  informe.fecha_registro

        if informe is None:
            return HttpResponse("No se encontró información del informe", status=404)

        workbook_main = Workbook()
        sheet = workbook_main.active
        sheet.title = f"Reporte de Cierre Diario: {informe.fecha_registro}"

        # Encabezados
        encabezados = [
            "#", "Nombre", "Total"
        ]
        for col_idx, header in enumerate(encabezados, start=1):
            sheet.cell(row=1, column=col_idx, value=header)

        

        registros = DetalleInformeDiario.objects.filter(reporte=informe)

        contador = 0

        for idx, registro in enumerate(registros, start=2):
            contador += 1
            

            fila = [contador,str( registro.tipo_datos),str(registro.cantidad)]

            for col_idx, value in enumerate(fila, start=1):
                sheet.cell(row=idx, column=col_idx, value=value)

            # Creacion individual del reporte
            cierre_diario_buffer = io.BytesIO()

            if registro.tipo_datos == 'clientes':
                wb_cliente = crear_excel_clientes(registro.data['clientes'], dia)
                wb_cliente.save(cierre_diario_buffer)
                cierre_diario_buffer.seek(0)
                zip_file.writestr(f"reporte_clientes.xlsx", cierre_diario_buffer.read())
            
            if registro.tipo_datos == 'creditos':
                wb_cliente = crear_excel_creditos(registro.data['creditos'], dia)
                wb_cliente.save(cierre_diario_buffer)
                cierre_diario_buffer.seek(0)
                zip_file.writestr(f"reporte_clientes.xlsx", cierre_diario_buffer.read())
                

        # Crear respuesta de descarga

        # 3. Guardar el Excel general en el zip
        main_excel_buffer = io.BytesIO()
        workbook_main.save(main_excel_buffer)
        main_excel_buffer.seek(0)
        zip_file.writestr("reporte_cierre_diario.xlsx", main_excel_buffer.read())

        zip_file.close()

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        response['Content-Disposition'] = f'attachment; filename="reporte_de_cierre_diario_{timestamp}.zip"'
        return response

