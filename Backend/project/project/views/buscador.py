# DECORADORES
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

# LIBRERIAS PARA CRUD
from django.views.generic import TemplateView
from django.db.models import Q

# APPs
from django.apps import apps

# MODELS
from django.db import models 

class Search(TemplateView):
    template_name = 'search.html'
    paginate_by = 25

    # Lista de aplicaciones cuyos modelos no queremos incluir en la búsqueda
    excluded_apps = [
        'auth', 
        'contenttypes', 
        'sessions', 
        'admin',
        'django_celery_beat',
    ]

    def get_queryset(self, model, query):
        """
        Obtiene el queryset filtrado para un modelo dado.
        """
        try:
            # Verificar si el campo es CharField o TextField
            fields = [field.name for field in model._meta.fields if isinstance(field, (models.CharField, models.TextField))]
            if fields:  
                query_filter = Q()
                for field in fields:
                    query_filter |= Q(**{f"{field}__icontains": query})
                return model.objects.filter(query_filter)
            return model.objects.none()  # Si no hay campos de texto
        except Exception as e:
            print(f"Error al filtrar el queryset para el modelo {model}: {e}")
            return model.objects.none()

    def query(self):
        """
        Obtiene el término de búsqueda de los parámetros GET.
        """
        return self.request.GET.get('q')

    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Construye el contexto para la plantilla con los resultados de búsqueda.
        """
        context = super().get_context_data(**kwargs)
        query = self.query()
        results = {}
        count = 0
        
        if query:
            # Obtener todos los modelos registrados en la aplicación
            all_models = apps.get_models()

            for model in all_models:
                # Excluir modelos que pertenezcan a las aplicaciones listadas en excluded_apps
                app_label = model._meta.app_label
                if app_label in self.excluded_apps:
                    continue  # Saltar este modelo

                # Filtrar los resultados para cada modelo
                model_results = self.get_queryset(model, query)
                if model_results.exists():
                    results[model._meta.verbose_name_plural] = model_results
                    count += model_results.count()

        context['query'] = query
        context['results'] = results
        context['count'] = count
        context['title'] = 'ELTELAR - Buscar'
        return context