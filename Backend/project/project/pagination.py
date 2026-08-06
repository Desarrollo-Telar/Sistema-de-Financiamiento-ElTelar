from django.core.paginator import Paginator

def paginacion(request, list):
    paginator = Paginator(list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Inyectamos el rango recortado directamente dentro de page_obj
    page_obj.custom_page_range = paginator.get_elided_page_range(
        page_obj.number, on_each_side=2, on_ends=1
    )
    
    return page_obj