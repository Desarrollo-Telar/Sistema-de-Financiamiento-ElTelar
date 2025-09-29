from django.db import models

# TIEMPO
from django.utils import timezone

# MODELOS

from .recibo import Recibo

# DECIMAL
from decimal import Decimal, InvalidOperation

# ESTADOS DE CUENTAS
class Invoice(models.Model):
    issue_date = models.DateField(default=timezone.now)
    numero_factura = models.IntegerField("Numero de Factura")
    recibo_id = models.ForeignKey(Recibo, on_delete=models.CASCADE, verbose_name="Recibo")
    numero_autorizacion = models.CharField(verbose_name="Número de Autorizacion", max_length=150, blank=True, null=True)
    nit_receptor = models.CharField(verbose_name='NIT RECEPTOR', max_length=150, blank=True, null=True)
    nombre_receptor = models.CharField(verbose_name="Nombre Receptor", max_length=150, blank=True, null=True)
    correo_receptor = models.CharField(verbose_name='Correo Receptor', max_length=150, blank=True, null=True)
    serie_autorizacion = models.CharField(verbose_name="Serie de Autorizacion", max_length=150, blank=True, null=True)
    xml_certificado  = models.TextField(verbose_name="Serie de Autorizacion", blank=True, null=True)

    def __str__(self):
        return f'{self.numero_factura}'
    
    def _get_customer(self):
       
        return getattr(self.recibo_id.pago.credit, "customer_id", None) if self.recibo_id and self.recibo_id.pago and self.recibo_id.pago.credit else None

    def _set_nombre_receptor(self):
        customer = self._get_customer()
        if customer:
            self.nombre_receptor = customer.get_full_name()
        else:
            self.nombre_receptor = None
        return self.nombre_receptor
    
    def _set_correo_receptor(self):
        customer = self._get_customer()
        if customer:
            self.correo_receptor = customer.get_email_customer()
        else:
            self.correo_receptor = None
        return self.correo_receptor

    def _set_nit_receptor(self):
        customer = self._get_customer()
        if customer:
            self.nit_receptor = customer.get_nit_customer()
        else:
            self.nit_receptor = None
        return self.nit_receptor

    def save(self, *args, **kwargs):        
        self._set_nombre_receptor()
        self._set_nit_receptor()
        self.__set_correo_receptor()
        super().save(*args, **kwargs)

    
    def calculo_monto_gravable(monto):
        try:
            monto_decimal = Decimal(monto)
            return monto_decimal / Decimal('1.12')
        except (InvalidOperation, TypeError):
            return Decimal('0.00')

    def calculo_monto_impuesto(self, monto):
        try:
            monto_gravable = self.calculo_monto_gravable(monto)
            return monto_gravable * Decimal('0.12')
        except (InvalidOperation, TypeError):
            return Decimal('0.00')
    
    def get_items(self):
        listado_items = []

        if self.recibo_id.interes_pagado > 0:
            contexto = {
                'Cantidad': 1,
                'Descripcion': 'PAGO DE INTERES',
                'PrecioUnitario': self.recibo_id.mora_pagada,
                'Precio': self.recibo_id.mora_pagada,
                'Descuento': 0,
                'OtrosDescuento': 0,
                'Total': self.recibo_id.mora_pagada,
                'Impuestos': {
                    'NombreCorto': 'IVA',
                    'CodigoUnidadGravable': 1,
                    'MontoGravable': self.calculo_monto_gravable(self.recibo_id.mora_pagada),
                    'MontoImpuesto': self.calculo_monto_impuesto(self.recibo_id.mora_pagada)
                }
            }
            listado_items.append(contexto)

        

        if self.recibo_id.mora_pagada > 0:
            contexto = {
                'Cantidad': 1,
                'Descripcion': 'OTROS GASTOS ADMINISTRATIVOS',
                'PrecioUnitario': self.recibo_id.mora_pagada,
                'Precio': self.recibo_id.mora_pagada,
                'Descuento': 0,
                'OtrosDescuento': 0,
                'Total': self.recibo_id.mora_pagada,
                'Impuestos': {
                    'NombreCorto': 'IVA',
                    'CodigoUnidadGravable': 1,
                    'MontoGravable': self.calculo_monto_gravable(self.recibo_id.mora_pagada),
                    'MontoImpuesto': self.calculo_monto_impuesto(self.recibo_id.mora_pagada)
                }
            }
            listado_items.append(contexto)
        
        return listado_items

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
