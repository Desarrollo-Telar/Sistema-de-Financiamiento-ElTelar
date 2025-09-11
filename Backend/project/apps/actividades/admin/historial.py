# admin.py
from django.contrib import admin
from apps.actividades.models import ModelHistory

@admin.register(ModelHistory)
class ModelHistoryAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'action', 'user', 'timestamp']
    list_filter = ['action', 'content_type', 'timestamp', 'user']
    search_fields = ['content_type', 'object_id', 'data', 'user__username']
    readonly_fields = ['content_type', 'object_id', 'action', 'data', 'changes', 'user', 'timestamp', 'notes']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Vista de solo lectura para el historial
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_delete'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)