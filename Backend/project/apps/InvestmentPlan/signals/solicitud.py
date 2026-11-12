
import re
# Signals
from django.db.models.signals import pre_save, post_save
from datetime import datetime

from apps.InvestmentPlan.models import InvestmentPlan, ExpedientePlanNotario
from apps.InvestmentPlan.models import Acta, DetalleActa

# Django
from django.dispatch import receiver

def validar_codigo(codigo: str) -> bool:
    patron = r"^0\d{1,2}-IIT0[1-9]\d*-\d{4}$"
    return bool(re.match(patron, codigo))


# Función para generar el código de plan de inversion basado en el Tipo de Producto o Servicio junto a la referencia del codigo de cliente
def generate_investment_plan_code(sucursal, counter):
    current_date = datetime.now()
    current_year = current_date.year 

    codigo_establecimiento = sucursal.codigo_establecimiento
    
    return f'0{codigo_establecimiento}-IIT0{counter}-{current_year}'

def generar_codigo(instance):
    counter = 1
    investment_plan_code = generate_investment_plan_code(instance.sucursal, counter)

        # Verificar si no existe un código igual, si no, generar uno nuevo
    while InvestmentPlan.objects.filter(investment_plan_code=investment_plan_code).exists():
        counter += 1
        investment_plan_code = generate_investment_plan_code(instance.sucursal, counter)

    instance.investment_plan_code = investment_plan_code


@receiver(pre_save, sender=InvestmentPlan)
def set_investment_plan_code(sender, instance, **kwargs):
    
    if not instance.investment_plan_code or instance.investment_plan_code == '':
        generar_codigo(instance)
        

    elif instance.pk and InvestmentPlan.objects.filter(pk=instance.pk).exists():
        current_investment_plan = InvestmentPlan.objects.get(pk=instance.pk)

        if current_investment_plan.type_of_product_or_service != instance.type_of_product_or_service:
            generar_codigo(instance)
        
        if not validar_codigo(instance.investment_plan_code):
            generar_codigo(instance)


@receiver(post_save, sender=InvestmentPlan)
def handle_investment_plan_approval(sender, instance, created, **kwargs):
    from apps.users.models import User
    from project.send_mail.correos_para_notarios import send_email_notario

    if created:
        acta_activa, acta_creado = Acta.objects.get_or_create(fecha_acta = datetime.now().date(), acta_activa=True)

        DetalleActa.objects.create(
            acta=acta_activa,
            solicitud_credito=instance
        )



    if instance.estado_aprobacion != "ACEPTADO":
        return

    

    if not instance.notarios:
        return

    ids_unicos = {
        notario["id"]
        for notario in instance.notarios
        if notario.get("id")
    }

    for id_notario in ids_unicos:
        try:
            user_notario = User.objects.get(id=id_notario)

            expediente, creado = ExpedientePlanNotario.objects.get_or_create(
                investment_plan=instance,
                notario=user_notario
            )

            if not creado:
                continue

            send_email_notario(
                user=user_notario,
                plan_inversion_id=instance.id,
                formato="formato_01",
                uuid=expediente.uuid
            )

        except User.DoesNotExist:
            continue


