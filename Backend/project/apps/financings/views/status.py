from django.http import JsonResponse
import asyncio
from apps.financings.tareas_ansicronicas import ver_cuotas_no_cargadas
async def async_view(request):
    
    return JsonResponse({'message': 'Vista asincrónica completada'})
