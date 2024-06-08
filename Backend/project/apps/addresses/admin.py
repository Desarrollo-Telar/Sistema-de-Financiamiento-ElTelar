from django.contrib import admin

from .models import Address, Coordinate

# Register your models here.
admin.site.register(Address)
admin.site.register(Coordinate)