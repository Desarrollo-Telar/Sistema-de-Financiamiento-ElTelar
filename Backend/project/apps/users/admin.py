from django.contrib import admin

from .models import User, UserRole
from .models import VerificationToken
# Register your models here.

admin.site.register(UserRole)
admin.site.register(VerificationToken)

"""
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name','last_name', 'username', 'email', 'password','type_identification','identification_number','telephone','status','gender','nationality','profile_pic')
    list_display = ('__str__', 'user_code','creation_date')
admin.site.register(User, UserAdmin)
"""

admin.site.register(User)
