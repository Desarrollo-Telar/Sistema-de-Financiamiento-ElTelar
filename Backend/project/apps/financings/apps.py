from django.apps import AppConfig

# MODELO
#from .models import PaymentPlan



class FinancingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.financings'

    def ready(self):
        import apps.financings.signals
        

        #cuotas = PaymentPlan.objects.filter(cuota_vencida=False)


