from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

# 1. Creamos una clase de paginación personalizada (opcional, para definir el tamaño)
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100 # Cuántos créditos enviar por página
    page_size_query_param = 'page_size'
    max_page_size = 1000