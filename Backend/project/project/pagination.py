# DJANGO
from django.core.paginator import Paginator

# PAGINACION
def paginacion(request,list):
    paginator = Paginator(list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj