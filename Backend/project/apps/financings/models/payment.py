from django.db import models

# DIAS
from datetime import datetime
from django.utils import timezone

# DECIMAL
from decimal import Decimal

# FORMATO
from apps.financings.formato import formatear_numero

# CALCULOS
from apps.financings.calculos import calculo_mora, calculo_interes

# FUNCIONES
from scripts.pagos.cuota_pagar import cuota_a_pagar
from scripts.pagos.identificar_siguiente_cuota import encontrando_siguiente_cuota
from scripts.pagos.proceso_de_pago import procesos_de_pago
from scripts.excepciones_propias import MiExcepcionPersonalizada
from scripts.pagos.sobre_que_pago_analizar import sobre_que_es_pago

# LOOGER
from apps.financings.clases.personality_logs import logger
import re

# MODELO
from .disbursement import Disbursement
from .credit import Credit
from .bank import Banco
from apps.customers.models import Customer
from apps.accountings.models import Creditor, Insurance

from django.db.models import Q

from project.settings import MEDIA_URL, STATIC_URL

#
from datetime import timedelta
from project.database_store import minio_client  # asegúrate de que esté importado correctamente

# PAGOS
class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('FALLIDO', 'Fallido'),
    ]
    
    TYPE_PAYMENT = [
        ('DESEMBOLSO','DESEMBOLSO'),
        ('CREDITO','CREDITO'),
        ('GASTO','GASTO'),
        ('COMPRA','COMPRA'),
        ('SEGURO','SEGURO'),
        ('INGRESO','INGRESO'),
        ('CLIENTE','CLIENTE'),
        ('ACREEDOR','ACREEDOR'),
        ('SEGURO','SEGURO'),
        ('EGRESO','EGRESO')
    ]
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Credito')
    disbursement = models.ForeignKey(Disbursement, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Desembolso')
    monto = models.DecimalField('Monto', max_digits=12, decimal_places=2)
    numero_referencia = models.CharField('Numero de Referencia', max_length=255, unique=True)
    fecha_emision = models.DateTimeField('Fecha de Emision', default=timezone.now)
    fecha_creacion = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    estado_transaccion = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDIENTE')
    descripcion = models.TextField(blank=True, null=True)
    mora = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interes = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interes_generado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital_generado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    boleta = models.FileField("Boleta",blank=True, null=True,upload_to='pagos/boletas/')
    tipo_pago = models.CharField('Tipo de Pago', choices=TYPE_PAYMENT, max_length=75, default='CREDITO')
    descripcion_estado = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    cliente = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True, blank=True, verbose_name="Cliente")
    acreedor = models.ForeignKey(Creditor, on_delete=models.CASCADE, related_name='payment', blank=True, null=True)
    seguro = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name='payment', blank=True, null=True)

    # Nuevos Atributos
    registro_ficticio = models.BooleanField("Registro Ficticio", default=False)

    def get_registro_ficticio(self):
        return f'SI ES UNA BOLETA FICTICIA' if self.registro_ficticio else f'NO ES UNA BOLETA FICTICIA'

    def boleta_para(self):
        mensaje = ''

        if self.cliente:
            mensaje = f'{self.cliente.get_full_name()}'
        
        if self.acreedor:
            mensaje = f'{self.acreedor.nombre_acreedor}'
        
        if self.seguro:
            mensaje = f'{self.seguro.nombre_acreedor}'
        
        if self.credit:
            mensaje = f'{self.credit.codigo_credito}'
        
        if self.disbursement:
            mensaje = f'Desembolso del credito: {self.disbursement.credit_id.codigo_credito}'

        return mensaje

    def Fmonto(self):
        return formatear_numero(self.monto)
    
    def fechaEmision(self):
        return datetime.strftime(self.fecha_emision,'%Y-%m-%d')

    def pago(self):
        return Payment.objects.get(id=self.id)
    
    def banco(self):
        referencia = None 
        if re.match(r".*-D\d*$", self.numero_referencia, re.IGNORECASE):
            referencia = re.sub(r"-D\d*$", "", self.numero_referencia, flags=re.IGNORECASE)
        else:
            referencia = self.numero_referencia
        
        return Banco.objects.get(referencia=referencia)

    def get_recibo(self):
        from .recibo import Recibo
        return Recibo
    
    def get_estado_cuenta(self):
        from .accountstatement import AccountStatement
        return AccountStatement
    
    def get_plan_pagos(self):
        from .payment_plan import PaymentPlan
        return PaymentPlan
    
    def get_document(self):
        try:
            return minio_client.presigned_get_object(
                bucket_name='asiatrip',
                object_name=self.boleta.name,  # ejemplo: documents/archivo.pdf
                expires=timedelta(minutes=30)
            )
        except Exception as e:
            return '{}{}'.format(MEDIA_URL,self.boleta)


    def _cuota_pagar(self):
        return cuota_a_pagar(self)
        
    def _siguiente_cuota(self):
        return encontrando_siguiente_cuota(self)
    
    def _calculo_intereses(self):
        interes = self._cuota_pagar().interest
        return interes

    def _calculo_mora(self):
        # Obtener la cuota actual asociada
        cuota = self._cuota_pagar()
        
        # Fecha de creación del pago
        fecha_creacion_pago = self.creation_date

        # Obtener información del banco
        info_banco = self.banco()
        
        if info_banco:
            # Fecha de creación del registro en el banco
            fecha_creacion_registro_banco = info_banco.creation_date
            print(fecha_creacion_registro_banco)
            print(fecha_creacion_pago)
            
            # Verificar si el registro del banco es anterior al pago
            if fecha_creacion_registro_banco > fecha_creacion_pago:
                # Ajustar mora si ya fue generada
                
                if cuota.mora_generado:
                    cuota.mora -= cuota.mora_generado
                    cuota.mora_generado = 0
                    cuota.cambios = True
                    cuota.save()  # Guardar los cambios en la base de datos
        
        
        

        # Retornar la mora actualizada
        return cuota.mora

    
    def _calcular_total(self):
        cuota = self._cuota_pagar()
        total = cuota.interest + cuota.mora
        return round(total)

    def realizar_pago(self):
        try:
            cuota = self._cuota_pagar()

            if cuota is None:
                print('Buscar a la siguiente cuota')
                cuota = self._siguiente_cuota()

            saldo_pendiente = cuota.saldo_pendiente

            if saldo_pendiente is None:
                raise MiExcepcionPersonalizada('No se puede continuar debido a que no se ha encontra una cuota asociada al pago', saldo_pendiente)
            
            mora = self._calculo_mora()
            interes = cuota.interest
            
            procesos_de_pago(self,saldo_pendiente, interes,mora)

        except MiExcepcionPersonalizada as e:
            print(f"Ocurrió un error: {e}")

        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
    

    def _registrar_pago(self, pagado_mora, pagado_interes,aporte_capital, saldo_pendiente, excedente):
        # ------------------------------------ #
        informacion = sobre_que_es_pago(self)

        # ------------------------------------ #
        pago = self.pago()
        cuota = self._cuota_pagar()
        siguiente = self._siguiente_cuota()

        # ------------------------------------ #
        cuota_a_actualizar = False
        descripcion_para_estado_cuenta = None

        

        


        if self.registro_ficticio:
            descripcion_para_estado_cuenta = 'PAGO PARA CANCELAR EL CREDITO'
        else:
            descripcion_para_estado_cuenta = 'PAGO DE CREDITO'
        
       
        

        # VERIFICAR SI YA EXISTE UN RECIBO ASOCIADO CON EL PAGO O GENERAR UNO NUEVO
        recibos = self.get_recibo().objects.filter(pago=pago)

        if not recibos.exists():
            # Creamos un nuevo recibo si no hay existentes
            recibo = self.get_recibo()(
                mora=cuota.mora,
                interes=cuota.interest,
                pago=pago,
                total=self.monto,
                aporte_capital=aporte_capital,
                interes_pagado=pagado_interes,
                mora_pagada=pagado_mora,
                fecha = pago.fecha_emision.date(),
                cliente=informacion['cliente'],
                cuota=cuota
            )
            
            recibo.save()
        
        # ACTUALIZACION DE LA CUOTA
        cuota.interest -=pagado_interes
        mora_existente = cuota.mora
        cuota.mora -= pagado_mora
        cuota.principal += aporte_capital
        cuota.saldo_pendiente = saldo_pendiente
        cuota.numero_referencia = self.numero_referencia
        cuota.interes_pagado += pagado_interes
        cuota.cambios = False

        if cuota.interest == 0:
            informacion['credito'].estados_fechas = True
            

        interes = calculo_interes(saldo_pendiente, informacion['tasa_interes'])

        if aporte_capital > 0:
            cuota.status = True

            capital_original = cuota.capital_generado

            if cuota.principal >= capital_original:
                informacion['credito'].estado_aportacion  = True
                
            else:
                informacion['credito'].estado_aportacion  = False
            
        
        cuota.save()
        informacion['credito'].save()

        # ACTUALIZAR EL PAGO PARA REFREGAR LA CANTIDA PAGADA
        pago.mora =  pagado_mora
        pago.interes =  pagado_interes
        pago.capital = aporte_capital
        pago.estado_transaccion = 'COMPLETADO'
        pago.save()


        # REFLEJAR EN EL ESTADO DE CUENTA
        estados_cuenta = self.get_estado_cuenta().objects.filter(payment=pago)
        # Definimos los datos que se asignarán a los estados de cuenta
        excedente_estado_cuenta = 0
        # --------------------------- #
        if excedente is not None:
           excedente_estado_cuenta = abs(excedente)
           informacion['credito'].excedente =  abs(excedente)
           
 
        datos_estado_cuenta = {
            'abono': self.monto,            
            'credit': informacion['credit'],
            'payment': pago,
            'interest_paid': pagado_interes,
            'late_fee_paid': pagado_mora,
            'capital_paid': aporte_capital,
            'numero_referencia': pago.numero_referencia,
            'saldo_pendiente':saldo_pendiente,
            'description':  descripcion_para_estado_cuenta,
            'acreedor': informacion['acreedor'],
            'seguro':informacion['seguro'],
            'excedente':excedente_estado_cuenta
        }

        

        if estados_cuenta.exists():
            for estado_cuenta in estados_cuenta:
                # Actualizamos cada estado de cuenta existente
                for key, value in datos_estado_cuenta.items():
                    setattr(estado_cuenta, key, value)
                #estado_cuenta.save()
        else:
            # Creamos un nuevo estado de cuenta si no hay existentes
            estado_cuenta = self.get_estado_cuenta()(**datos_estado_cuenta)
            estado_cuenta.save()
        
        
           
            


        # VERIFICAR SI EL CREDITO YA FUE PAGADO POR COMPLETO
        if saldo_pendiente <= 0:
            saldo_pendiente = 0

            informacion['credito'].is_paid_off = True
            informacion['credito'].saldo_pendiente  = 0
            informacion['credito'].estado_aportacion = True
            informacion['credito'].estados_fechas = True
            informacion['credito'].save()
            

            if siguiente is not None:
                siguiente.delete()

            return f'EL CREDITO PAGADO COMPLETAMENTE'
        
        informacion['credito'].saldo_pendiente  = saldo_pendiente
        informacion['credito'].saldo_actual   = saldo_pendiente + cuota.mora + cuota.interest
        informacion['credito'].save()

        if siguiente is not None:
            # Actualizamos la siguiente cuota si ya existe
            cuota_a_actualizar = siguiente
            print(f'LA CUOTA: {siguiente}\nREALIZA CAMBIOS SOBRE:\nINTERES ANTIGUO: {cuota_a_actualizar.interest}\nMORA ANTIGUA: {cuota_a_actualizar.mora}\nSALDO PENDIENTE: {cuota_a_actualizar.saldo_pendiente}')
            cuota_a_actualizar.cambios = True
            
            if cuota.interest <=0:
                cuota_a_actualizar.interest =  interes
                
            else:
                cuota_a_actualizar.interest  = max (0, cuota_a_actualizar.interest - pagado_interes)
            
            if cuota.mora == 0:
                cuota_a_actualizar.mora = 0
                cuota_a_actualizar.mora_generado = 0
            else:
                cuota_a_actualizar.mora = Decimal(cuota_a_actualizar.interest) * Decimal(0.1)  
                cuota_a_actualizar.mora_generado = Decimal(cuota_a_actualizar.interest) * Decimal(0.1)
                
        else:
            print('CREACION DE UNA NUEVA  CUOTA')
            
            
                

        # En ambos casos (cuota nueva o existente), actualizamos los campos comunes
        if cuota_a_actualizar is not None:
            cuota_a_actualizar.start_date = cuota.due_date
            cuota_a_actualizar.saldo_pendiente = saldo_pendiente
            cuota_a_actualizar.credit_id = informacion['credit']
            cuota_a_actualizar.acreedor = informacion['acreedor']
            cuota_a_actualizar.seguro = informacion['seguro']
            cuota_a_actualizar.outstanding_balance = saldo_pendiente

            informacion['credito'].saldo_actual   = saldo_pendiente + cuota_a_actualizar.mora + cuota_a_actualizar.interest
            informacion['credito'].save()
            
            
            
            print(f'LA CUOTA: {siguiente}\nREALIZA CAMBIOS SOBRE:\nINTERES NUEVO: {cuota_a_actualizar.interest}\nMORA NUEVA: {cuota_a_actualizar.mora}\nSALDO PENDIENTE: {saldo_pendiente}')
            

            # Guardamos los cambios
            #if cuota_a_actualizar:
            cuota_a_actualizar.save()


    def __str__(self):
        return f'PAGO {self.numero_referencia} - {self.estado_transaccion}'

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'