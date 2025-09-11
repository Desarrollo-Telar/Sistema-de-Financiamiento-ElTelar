# mixins.py
from django.urls import reverse
from django.utils.html import format_html

class HistoryMixin:
    """Mixin para agregar funcionalidad de historial a cualquier modelo"""
    
    def get_history(self):
        """Obtiene el historial de este objeto"""
        from apps.actividades.models import ModelHistory
        return ModelHistory.objects.filter(
            content_type=self._meta.label,
            object_id=self.pk
        ).order_by('-timestamp')
    
    def history_link(self):
        """Enlace al historial para admin"""
        from django.utils.html import format_html
        count = self.get_history().count()
        url = reverse('admin:app_modelhistory_changelist') + f'?object_id={self.pk}&content_type={self._meta.label}'
        return format_html('<a href="{}">Ver historial ({} cambios)</a>', url, count)
    
    history_link.short_description = 'Historial'