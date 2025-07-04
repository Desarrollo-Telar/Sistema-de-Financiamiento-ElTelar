# Register your models here.

# FORMULARIO
from apps.users.forms import CustomUserChangeForm, UserCreationForm

# ADMIN
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# MODELO
from apps.users.models import User


class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff','rol')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'type_identification', 'identification_number', 'telephone', 'gender', 'user_code', 'nationality', 'profile_pic', 'rol','status')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'type_identification', 'identification_number', 'telephone', 'status', 'gender', 'user_code', 'nationality', 'profile_pic','rol'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username', 'email')

USUARIOADMINISTRADOR = admin.site.register(User, CustomUserAdmin)