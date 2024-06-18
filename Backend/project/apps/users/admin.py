from django.contrib import admin

from .models import User


from django.contrib.auth.models import Permission

# Register your models here.
from .forms import CustomUserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


admin.site.register(Permission)

class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'type_identification', 'identification_number', 'telephone', 'gender', 'user_code', 'nationality', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'type_identification', 'identification_number', 'telephone', 'status', 'gender', 'user_code', 'nationality', 'profile_pic'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username', 'email')

admin.site.register(User, CustomUserAdmin)

