from django.contrib import admin

from .models import WorkingInformation, OtherSourcesOfIncome, Reference
# Register your models here.

admin.site.register(WorkingInformation)
admin.site.register(OtherSourcesOfIncome)
admin.site.register(Reference)