# ADMIN
from django.contrib import admin

# MODELO
from apps.roles.models import Role

@admin.register(Role)
class RoleAdministrador(admin.ModelAdmin):
    fields = ('role_name','description')