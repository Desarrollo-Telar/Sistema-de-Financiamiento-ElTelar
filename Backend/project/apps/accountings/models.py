from django.db import models
from dateutil.relativedelta import relativedelta
# Create your models here.
# FORMATO
from apps.financings.formato import formatear_numero

# RELACIONES
from apps.financings.models import Credit

from project.settings import MEDIA_URL, STATIC_URL
from project.database_store import minio_client  # asegúrate de que esté importado correctamente
from datetime import timedelta
# Acreedor
class Creditor(models.Model):
    codigo_acreedor = models.CharField("Codigo de Acreedor", max_length=100) # AC-2024-001
    nombre_acreedor = models.CharField("Nombre del Acreedor", max_length=150)
    fecha_inicio = models.DateField("Fecha de Inicio", blank=False, null=False)
    monto = models.DecimalField("Monto", decimal_places=2, max_digits=15, blank=False, null=False)
    tasa = models.DecimalField("Tasa", max_digits=5, decimal_places=3, null=False, blank=False)
    plazo = models.IntegerField("Plazo", blank=False, null=False)
    fecha_vencimiento = models.DateField("Fecha de Vencimiento", blank=False, null=False)
    fecha_registro = models.DateField("Fecha de registro",auto_now_add=True)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, blank=True, null=True)
    observaciones = models.TextField("Observaciones",blank=True, null=True)
    boleta = models.FileField("Boleta",blank=True, null=True,upload_to='pagos/boletas/acreedor/')
    status = models.BooleanField("Status",default=False)
    saldo_pendiente = models.DecimalField("Saldo Pendiente", decimal_places=2, max_digits=15, default=0)
    saldo_actual = models.DecimalField("Saldo Actual", decimal_places=2, max_digits=15, default=0)
    is_paid_off = models.BooleanField(default=False)
    estado_aportacion = models.BooleanField(blank=True, null=True)
    estados_fechas =  models.BooleanField(blank=True, null=True)
    forma_de_pago = models.CharField("Forma de Pago", max_length=75, blank=False, null=False, default='AMORTIZACIONES A CAPITAL')
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True,blank=True, null=True)
    excedente = models.DecimalField("Monto de excedente", decimal_places=2, max_digits=15, blank=True, null=True, default=0)

    def get_boleta(self):
        return '{}{}'.format(MEDIA_URL,self.boleta)

    def fmonto(self):
        return formatear_numero(self.monto)
    
    def ftasa(self):
        convertir =  self.tasa *100
        return formatear_numero(convertir)

    def formato_estado_aportacion(self):
        mensaje = None
        if self.estado_aportacion:
            mensaje = 'VIGENTE'
        elif self.estado_aportacion is None:
            mensaje = 'SIN APORTACIONES'
        else:
            mensaje = 'EN ATRASO'

        return mensaje
    
    def formato_estado_fecha(self):
        return 'VIGENTE' if self.estados_fechas else 'EN ATRASO'
    
    def formato_credito_cancelado(self):
        return 'CANCELADO' if self.is_paid_off else 'VIGENTE'
    
    def formato_saldo_actual(self):
        return formatear_numero(self.saldo_actual)
        

    def calcular_fecha_vencimiento(self):
        self.fecha_vencimiento = self.fecha_inicio + relativedelta(months=self.plazo)
        return self.fecha_vencimiento

    def save(self, *args, **kwargs):
        self.calcular_fecha_vencimiento()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.codigo_acreedor} {self.nombre_acreedor}'

    class Meta:
        verbose_name = "Acreedor"
        verbose_name_plural = "Acreedores"

# Seguro
class Insurance(models.Model):
    codigo_seguro = models.CharField("Codigo de Seguro", max_length=100) # SEG-2024-001
    nombre_acreedor = models.CharField("Nombre", max_length=150)
    fecha_inicio = models.DateField("Fecha de Inicio", blank=False, null=False)
    monto = models.DecimalField("Monto", decimal_places=2, max_digits=15, blank=False, null=False)
    tasa = models.DecimalField("Tasa", max_digits=5, decimal_places=3, null=False, blank=False)
    plazo = models.IntegerField("Plazo", blank=False, null=False)
    fecha_vencimiento = models.DateField("Fecha de Vencimiento", blank=False, null=False)
    fecha_registro = models.DateField("Fecha de registro",auto_now_add=True)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, blank=True)
    observaciones = models.TextField("Observaciones",blank=True, null=True)
    boleta = models.FileField("Boleta",blank=True, null=True,upload_to='pagos/boletas/acreedor/')
    status = models.BooleanField("Status",default=False)
    saldo_pendiente = models.DecimalField("Saldo Pendiente", decimal_places=2, max_digits=15, default=0)
    saldo_actual = models.DecimalField("Saldo Actual", decimal_places=2, max_digits=15, default=0)
    is_paid_off = models.BooleanField(default=False)
    estado_aportacion = models.BooleanField(blank=True, null=True)
    estados_fechas =  models.BooleanField(blank=True, null=True)
    forma_de_pago = models.CharField("Forma de Pago",  max_length=75, blank=False, null=False, default='AMORTIZACIONES A CAPITAL')
    credito = models.ForeignKey(Credit, on_delete=models.CASCADE, blank=True, null=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True,blank=True, null=True)
    excedente = models.DecimalField("Monto de excedente", decimal_places=2, max_digits=15, blank=True, null=True, default=0)

    def get_boleta(self):
        return '{}{}'.format(MEDIA_URL,self.boleta)

    def fmonto(self):
        return formatear_numero(self.monto)
    
    def formato_saldo_actual(self):
        return formatear_numero(self.saldo_actual)
    
    def nombre_por_seguro(self):
        return self.nombre_acreedor
    
    def formato_estado_aportacion(self):
        mensaje = None
        if self.estado_aportacion:
            mensaje = 'VIGENTE'
        elif self.estado_aportacion is None:
            mensaje = 'SIN APORTACIONES'
        else:
            mensaje = 'EN ATRASO'

        return mensaje
    
    def formato_estado_fecha(self):
        return 'VIGENTE' if self.estados_fechas else 'EN ATRASO'
    
    def formato_credito_cancelado(self):
        return 'CANCELADO' if self.is_paid_off else 'VIGENTE'
    
    def ftasa(self):
        convertir =  self.tasa *100
        return formatear_numero(convertir)
        

    def calcular_fecha_vencimiento(self):
        self.fecha_vencimiento = self.fecha_inicio + relativedelta(months=self.plazo)
        return self.fecha_vencimiento

    def save(self, *args, **kwargs):
        self.calcular_fecha_vencimiento()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.codigo_seguro} {self.nombre_acreedor}'

    class Meta:
        verbose_name = "Seguro"
        verbose_name_plural = "Seguros"

# Ingreso
class Income(models.Model):
    fecha = models.DateField("Fecha", blank=False, null=False)
    monto = models.DecimalField("Monto", decimal_places=2, max_digits=15, blank=False, null=False) 
    codigo_ingreso = models.CharField("Codigo de Ingreso", max_length=100) # TIPOS DE INGRESOS 
    descripcion = models.TextField("Descripcion",blank=True, null=True)
    observaciones = models.TextField("Observaciones",blank=True, null=True)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, unique=True)
    boleta = models.FileField("Boleta",blank=True, null=True,upload_to='pagos/boletas/otros_ingresos/')
    status = models.BooleanField("Status",default=False)
    fecha_registro = models.DateField("Fecha de registro",auto_now_add=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True,blank=True, null=True)

    def get_boleta(self):
        return '{}{}'.format(MEDIA_URL,self.boleta)

    def fmonto(self):
        return formatear_numero(self.monto)

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"

# Egreso
class Egress(models.Model):
    fecha = models.DateField("Fecha", blank=False, null=False)
    fecha_doc_fiscal = models.DateField("Fecha De Documento Fiscal", blank=True, null=True)
    numero_doc = models.CharField("Numero De Documento Fiscal", max_length=155,blank=True, null=True)
    nit = models.CharField("Numero De Documento Fiscal", max_length=50,blank=True, null=True)
    monto = models.DecimalField("Monto", decimal_places=2, max_digits=15, blank=False, null=True)
    monto_doc = models.DecimalField("Monto del Documento", decimal_places=2, max_digits=15, blank=False, null=True)
    codigo_egreso = models.CharField("Codigo de Egreso", max_length=100) # TIPOS DE EGRESOS ( GASTOS )
    descripcion = models.TextField("Descripcion",blank=True, null=True)
    observaciones = models.TextField("Observaciones",blank=True, null=True)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, unique=True)
    boleta = models.FileField("Boleta",blank=True, null=True,upload_to='pagos/boletas/gasto/')
    documento = models.FileField("Documento",blank=True, null=True,upload_to='pagos/boletas/gasto/documento/')
    status = models.BooleanField("Status",default=False)
    fecha_registro = models.DateField("Fecha de registro",auto_now_add=True)

    # NUEVOS ATRIBUTOS
    nombre = models.CharField("Nombre de Colaborador", max_length=150, null=True, blank=True)
    pago_correspondiente = models.CharField("Pago Correspondiente", blank=True, null=True, max_length=150)
    tipo_impuesto = models.CharField("Tipo de Impuesto", blank=True, null=True, max_length=150)
    
    # MAS ATRIBUTOS NUEVOS
    acreedor = models.ForeignKey(Creditor, on_delete=models.CASCADE, related_name='egress', blank=True, null=True)
    seguro = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name='egress', blank=True, null=True)
    tipo_gasto = models.CharField("Tipo de Gasto", blank=True, null=True, max_length=150)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True,blank=True, null=True)

    def get_boleta(self):
        try:
            return minio_client.presigned_get_object(
                bucket_name='asiatrip',
                object_name=self.boleta.name,  # ejemplo: documents/archivo.pdf
                expires=timedelta(minutes=30)
            )
        except Exception as e:
            return '{}{}'.format(MEDIA_URL,self.boleta)

    def get_documento(self):
        try:
            return minio_client.presigned_get_object(
                bucket_name='asiatrip',
                object_name=self.documento.name,  # ejemplo: documents/archivo.pdf
                expires=timedelta(minutes=30)
            )
        except Exception as e:
            return '{}{}'.format(MEDIA_URL,self.documento)

    def fmonto(self):
        return formatear_numero(self.monto)
    
    def fmontoD(self):
        return formatear_numero(self.monto)

    class Meta:
        verbose_name = "Egreso"
        verbose_name_plural = "Egresos"
