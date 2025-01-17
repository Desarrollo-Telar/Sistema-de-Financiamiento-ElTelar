from django.db import models

# Create your models here.

# Acreedor
class Creditor(models.Model):
    codigo_acreedor = models.CharField("Codigo de Acreedor", max_length=100)
    nombre_acreedor = models.CharField("Nombre del Acreedor", max_length=150)
    fecha_inicio = models.DateField("Fecha de Inicio", blank=False, null=False)
    monto = models.DecimalField("Monto", decimal_places=2, max_digits=15, blank=False, null=False)
    tasa = models.DecimalField("Tasa", max_digits=5, decimal_places=3, null=False, blank=False)
    plazo = models.IntegerField("Plazo", blank=False, null=False)
    fecha_vencimiento = models.DateField("Fecha de Vencimiento", blank=False, null=False)
    fecha_registro = models.DateField("Fecha de registro",auto_now_add=True)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, unique=True)
    observaciones = models.TextField("Observaciones",blank=True, null=True)
    boleta = models.FileField("Boleta",blank=True, null=True,upload_to='pagos/boletas/acreedor/')
    status = models.BooleanField("Status",default=False)

# Seguro
class Insurance(models.Model):
    codigo_seguro = models.CharField("Codigo de Seguro", max_length=100)
    nombre_acreedor = models.CharField("Nombre", max_length=150)
    fecha_inicio = models.DateField("Fecha de Inicio", blank=False, null=False)
    monto = models.DecimalField("Monto", decimal_places=2, max_digits=15, blank=False, null=False)
    tasa = models.DecimalField("Tasa", max_digits=5, decimal_places=3, null=False, blank=False)
    plazo = models.IntegerField("Plazo", blank=False, null=False)
    fecha_vencimiento = models.DateField("Fecha de Vencimiento", blank=False, null=False)
    fecha_registro = models.DateField("Fecha de registro",auto_now_add=True)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, unique=True)
    observaciones = models.TextField("Observaciones",blank=True, null=True)
    boleta = models.FileField("Boleta",blank=True, null=True,upload_to='pagos/boletas/acreedor/')
    status = models.BooleanField("Status",default=False)

# Ingreso
class Income(models.Model):
    fecha = models.DateField("Fecha", blank=False, null=False)
    monto = models.DecimalField("Monto", decimal_places=2, max_digits=15, blank=False, null=False)
    codigo_ingreso = models.CharField("Codigo de Ingreso", max_length=100)
    descripcion = models.TextField("Descripcion",blank=True, null=True)
    observaciones = models.TextField("Observaciones",blank=True, null=True)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, unique=True)
    boleta = models.FileField("Boleta",blank=True, null=True,upload_to='pagos/boletas/otros_ingresos/')
    status = models.BooleanField("Status",default=False)
    fecha_registro = models.DateField("Fecha de registro",auto_now_add=True)

# Egreso
class Egress(models.Model):
    fecha = models.DateField("Fecha", blank=False, null=False)
    fecha_doc_fiscal = models.DateField("Fecha De Documento Fiscal", blank=True, null=True)
    numero_doc = models.CharField("Numero De Documento Fiscal", max_length=155,blank=True, null=True)
    nit = models.CharField("Numero De Documento Fiscal", max_length=50,blank=True, null=True)
    monto = models.DecimalField("Monto", decimal_places=2, max_digits=15, blank=False, null=False)
    monto_doc = models.DecimalField("Monto del Documento", decimal_places=2, max_digits=15, blank=False, null=False)
    codigo_ingreso = models.CharField("Codigo de Ingreso", max_length=100)
    descripcion = models.TextField("Descripcion",blank=True, null=True)
    observaciones = models.TextField("Observaciones",blank=True, null=True)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, unique=True)
    boleta = models.FileField("Boleta",blank=True, null=True,upload_to='pagos/boletas/gasto/')
    documento = models.FileField("Boleta",blank=True, null=True,upload_to='pagos/boletas/gasto/documento/')
    status = models.BooleanField("Status",default=False)
    fecha_registro = models.DateField("Fecha de registro",auto_now_add=True)
