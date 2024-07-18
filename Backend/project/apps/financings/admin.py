from django.contrib import admin

from apps.financings.models import Credit, Guarantees, DetailsGuarantees
# Register your models here.
admin.site.register(Credit)
admin.site.register(Guarantees)
admin.site.register(DetailsGuarantees)