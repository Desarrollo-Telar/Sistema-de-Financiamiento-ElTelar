from django.contrib import admin

from .models import User, UserRole
from .models import VerificationToken

from django.contrib.auth.models import Permission

# Register your models here.

admin.site.register(UserRole)
admin.site.register(VerificationToken)
admin.site.register(Permission)

admin.site.register(User)
