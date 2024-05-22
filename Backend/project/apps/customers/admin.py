from django.contrib import admin

from .models import Customer, ImmigrationStatus

# Register your models here.
admin.site.register(Customer)
admin.site.register(ImmigrationStatus)