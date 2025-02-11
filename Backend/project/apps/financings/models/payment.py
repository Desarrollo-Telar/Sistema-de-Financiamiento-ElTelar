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

# LOOGER
from apps.financings.clases.personality_logs import logger


# MODELO
from .disbursement import Disbursement
from .credit import Credit
from .bank import Banco
from apps.customers.models import Customer
from apps.accountings.models import Creditor, Insurance

from django.db.models import Q

from project.settings import MEDIA_URL, STATIC_URL

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

    # Nuevos atributos
    cliente = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True, blank=True, verbose_name="Cliente")
    acreedor = models.ForeignKey(Creditor, on_delete=models.CASCADE, related_name='payment', blank=True, null=True)
    seguro = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name='payment', blank=True, null=True)

    def Fmonto(self):
        return formatear_numero(self.monto)
    
    def fechaEmision(self):
        return datetime.strftime(self.fecha_emision,'%Y-%m-%d')

    def pago(self):
        return Payment.objects.get(id=self.id)
    
    def banco(self):
        return Banco.objects.get(referencia=self.numero_referencia)

    def credito(self):
        if self.credit:
            return Credit.objects.get(id=self.credit.id)
        return None
    
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
        return '{}{}'.format(MEDIA_URL,self.boleta)


    def _cuota_pagar(self):
        """
        Encuentra la próxima cuota a pagar en función de la fecha de emisión y el historial de pagos.
        """
        # Obtener todas las cuotas del crédito ordenadas por la fecha límite
        cuotas = None
        historial_a = None
        cuota_a_pagar = None

        if self.credit is not None:
            cuotas = self.get_plan_pagos().objects.filter(credit_id=self.credit).order_by('fecha_limite')
            # Historial de pagos anteriores (último pago realizado)
            historial_a = self.get_estado_cuenta().objects.filter(credit=self.credit, description='PAGO DE CREDITO').order_by('-id').first()
            cuota_a_pagar = self.get_plan_pagos().objects.filter(credit_id=self.credit.id).order_by('-id').first()
        
        if self.acreedor is not None:
            cuotas = self.get_plan_pagos().objects.filter(acreedor=self.acreedor).order_by('fecha_limite')
            # Historial de pagos anteriores (último pago realizado)
            historial_a = self.get_estado_cuenta().objects.filter(acreedor=self.acreedor, description='PAGO DE ACREEDOR').order_by('-id').first()
            cuota_a_pagar = self.get_plan_pagos().objects.filter(acreedor=self.acreedor.id).order_by('-id').first()
        
        if self.seguro is not None:
            cuotas = self.get_plan_pagos().objects.filter(acreedor=self.acreedor).order_by('fecha_limite')
            # Historial de pagos anteriores (último pago realizado)
            historial_a = self.get_estado_cuenta().objects.filter(seguro=self.seguro, description='PAGO DE SEGURO').order_by('-id').first()
            cuota_a_pagar = self.get_plan_pagos().objects.filter(seguro=self.seguro.id).order_by('-id').first()


        # Fecha de emisión (como objeto datetime)
        fecha_emision = self.fecha_emision
        logger.info(f"Fecha de emisión: {fecha_emision}")

       

        # Verifica si hay historial de pagos
        if historial_a:
            ultima_fecha = historial_a.payment.fecha_emision
            logger.info(f"Última fecha de pago: {ultima_fecha}")

            # Calcular la diferencia en días
            diferencia = (ultima_fecha - fecha_emision).days
            logger.info(f"Diferencia en días desde el último pago: {diferencia} días")

            # Si han pasado 15 días desde el último pago
            if diferencia >= 15:
                # Devolver la cuota más reciente impaga
                logger.info('COBRANDO LA ULTIMA CUOTA POR DIFERENCIA DE DÍAS >= 15')
                
                return cuota_a_pagar

        else:
            logger.info("No hay historial de pagos")

        # Si no han pasado 31 días, se recorre las cuotas por fechas
        logger.info("Pasando a comparar cuotas por rangos de fechas")

        # Recorre las cuotas para realizar las comparaciones por fechas
        for cuota in cuotas:
            # Usar objetos datetime directamente
            fecha_inicio = cuota.start_date
            fecha_limite = cuota.fecha_limite
            logger.info(f"Comparando cuota con rango: {fecha_inicio} a {fecha_limite}")
                        
            # Comparar directamente objetos datetime
            if fecha_inicio <= fecha_emision <= fecha_limite:
                # Si la fecha de emisión cae dentro del rango de esta cuota
                logger.info("Cuota encontrada en rango de fechas")
                if fecha_emision == fecha_limite:
                    logger.info("Fecha de emisión es igual a la fecha límite, continuando a la siguiente cuota")
                    continue 
                return cuota

        # Si no se encuentra ninguna cuota aplicable
        logger.info("No se encontró ninguna cuota aplicable")
        return None

    def _siguiente_cuota(self):
        """
        Devuelve la siguiente cuota después de la cuota a pagar actual.
        """
        # Obtener la cuota actual a pagar
        cuota_actual = self._cuota_pagar()
        cuotas = None
        if cuota_actual:
            # Obtener todas las cuotas ordenadas por fecha límite
            if self.credit:
                cuotas = self.get_plan_pagos().objects.filter(
                    Q(credit_id=self.credit)
                ).order_by('fecha_limite')
                # Historial de pagos anteriores (último pago realizado)
                historial_a = self.get_estado_cuenta().objects.filter(credit=self.credit, description='PAGO DE CREDITO').order_by('-id').first()
                cuota_a_pagar = self.get_plan_pagos().objects.filter(credit_id=self.credit.id).order_by('-id').first()
            
            if self.acreedor:
                cuotas = self.get_plan_pagos().objects.filter(
                    Q(acreedor=self.acreedor)
                ).order_by('fecha_limite')
                # Historial de pagos anteriores (último pago realizado)
                historial_a = self.get_estado_cuenta().objects.filter(acreedor=self.acreedor, description='PAGO DE ACREEDOR').order_by('-id').first()
                cuota_a_pagar = self.get_plan_pagos().objects.filter(acreedor=self.acreedor.id).order_by('-id').first()
            
            if self.seguro:
                cuotas = self.get_plan_pagos().objects.filter(
                    Q(acreedor=self.acreedor)
                ).order_by('fecha_limite')
                # Historial de pagos anteriores (último pago realizado)
                historial_a = self.get_estado_cuenta().objects.filter(seguro=self.seguro, description='PAGO DE SEGURO').order_by('-id').first()
                cuota_a_pagar = self.get_plan_pagos().objects.filter(seguro=self.seguro.id).order_by('-id').first()
            
           
            
            # Iterar sobre las cuotas después de la cuota actual
            encontrada = False
            for cuota in cuotas:
                if encontrada:
                    # Si ya encontramos la cuota actual, la siguiente será la segunda cuota
                    if cuota == cuota_actual:
                        return None
                    return cuota
                
                if cuota == cuota_actual:
                    # Marcamos que encontramos la cuota actual
                    encontrada = True

        return None  # Si no existe una siguiente cuota

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
        print('realizando el pago')
        cuota = self._cuota_pagar()
        
        if cuota is None:
            logger.error(f'NO SE HA ENCONTRADO NINGUNA CUOTA')
            cuota = self._siguiente_cuota()
            #return f'CUOTA NO ENCONTRADA'

        saldo_pendiente = None

        if self.credito() is not None:
            saldo_pendiente = self.credito().saldo_pendiente
        elif self.acreedor is not None:
            saldo_pendiente = self.acreedor.saldo_pendiente
        
        elif self.seguro is not None:
            saldo_pendiente = self.seguro.saldo_pendiente
        
        mora = self._calculo_mora()
        interes = self._calculo_intereses()
        
        monto_depositado = self.monto

        pagado_mora = 0
        pagado_interes = 0
        aporte_capital = 0

        def procesar_pago(tipo, monto_requerido):
            nonlocal monto_depositado, pagado_mora, pagado_interes

            if monto_depositado >= monto_requerido:
                monto_depositado = round(monto_depositado - monto_requerido, 2)
                
                if tipo == 'Mora':
                    pagado_mora += monto_requerido
                elif tipo == 'Interes':
                    pagado_interes += monto_requerido

                return 0
            else:
                saldo = round(monto_requerido - monto_depositado, 2)
                
                if tipo == 'Mora':
                    pagado_mora += monto_depositado
                elif tipo == 'Interes':
                    pagado_interes += monto_depositado

                monto_depositado = 0    
                return saldo
        
        

        # Procesar pago de mora
        mora = procesar_pago('Mora', mora) 
        if mora > 0:
            aporte_capital = monto_depositado       
            self._registrar_pago(pagado_mora=pagado_mora, pagado_interes=pagado_interes,aporte_capital=aporte_capital,saldo_pendiente=saldo_pendiente)
            return f"Pago realizado parcialmente. Quedan Q{mora} de mora pendiente. "

       
        # Procesar pago de intereses
        interes = procesar_pago('Interes', interes)
        
        if interes > 0:
            aporte_capital = monto_depositado
            self._registrar_pago(pagado_mora=pagado_mora, pagado_interes=pagado_interes,aporte_capital=aporte_capital,saldo_pendiente=saldo_pendiente)
            return f"Pago realizado parcialmente. Quedan Q{interes} de intereses pendientes. "
        
        aporte_capital = monto_depositado
        saldo_pendiente -= aporte_capital
        self._registrar_pago(pagado_mora=pagado_mora, pagado_interes=pagado_interes,aporte_capital=aporte_capital,saldo_pendiente=saldo_pendiente)
        return f"Pago realizado con éxito. Q{self.monto} restante. Saldo pendiente total: Q{saldo_pendiente}"
    

    def _registrar_pago(self, pagado_mora, pagado_interes,aporte_capital, saldo_pendiente):
        credito = self.credito()
        acreedor = self.acreedor
        seguro = self.seguro
        pago = self.pago()
        cuota = self._cuota_pagar()
        siguiente = self._siguiente_cuota()
        cuota_a_actualizar = False
        descripcion = None
        tasa_interes = None

        # SE GENERA EL RECIBO
        """
        VERIFICAR SI YA EXISTE UN RECIBO ASOCIADO CON EL PAGO O GENERAR UNO NUEVO
        """
        
        recibos = self.get_recibo().objects.filter(pago=pago)
        cliente = None
        if credito is not None:
            descripcion = 'PAGO DE CREDITO'
            tasa_interes = credito.tasa_interes
            cliente=credito.customer_id

        if acreedor is not None:
            descripcion = 'PAGO PARA EL ACREEDOR'
            tasa_interes = self.acreedor.tasa

        if seguro is not None:
            descripcion = 'PAGO PARA EL SEGURO'
            tasa_interes = self.seguro.tasa
    
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
                
                cliente=cliente,
                cuota=cuota
            )
            
            recibo.save()
       

        # ACTUALIZAR LA CUOTA QUE SE ESTA CREANDO 
                            # 500 - 100 = 400
        logger.info('CAMBIOS EN SOBRE CUOTA, DESDE EL PAGO')
        logger.info(f'''
        {cuota.interest}
        {cuota.mora}
        {cuota.principal}
        
        ''')
        cuota.interest -=pagado_interes
        mora_existente = cuota.mora
        cuota.mora -= pagado_mora
        cuota.principal += aporte_capital
        cuota.saldo_pendiente = saldo_pendiente
        cuota.numero_referencia = self.numero_referencia
        cuota.interes_pagado += pagado_interes
        cuota.cambios = False
        logger.info(f'''
        CUOTA ACTUALIZADA
        {cuota.interest}
        {cuota.mora}
        {cuota.principal}
        
        
        ''')
        
        interes = calculo_interes(saldo_pendiente, tasa_interes)
        if aporte_capital > 0:
            cuota.status = True
            #cuota_a_actualizar = self.get_plan_pagos()()
            #cuota_a_actualizar.interest =  interes
            #cuota_a_actualizar.interes_generado =  interes
            capital_original = cuota.capital_generado

            if cuota.principal >= capital_original:
                if credito is not None:
                    credito.estado_aportacion = True

                if acreedor is not None:
                    acreedor.estado_aportacion = True

                if seguro is not None:
                    seguro.estado_aportacion = True
                
                
            else:
                if credito is not None:
                    credito.estado_aportacion = False

                if acreedor is not None:
                    acreedor.estado_aportacion = False

                if seguro is not None:
                    seguro.estado_aportacion = False
                
            
        cuota.save()


        # ACTUALIZAR EL PAGO PARA REFREGAR LA CANTIDA PAGADA
        pago.mora =  pagado_mora
        pago.interes =  pagado_interes
        pago.capital = aporte_capital
        pago.estado_transaccion = 'COMPLETADO'
        pago.save()

        # REFLEJAR EN EL ESTADO DE CUENTA
        estados_cuenta = self.get_estado_cuenta().objects.filter(payment=pago)

        # Definimos los datos que se asignarán a los estados de cuenta
        

        

        datos_estado_cuenta = {
            'abono': self.monto,            
            'credit': credito,
            'payment': pago,
            'interest_paid': pagado_interes,
            'late_fee_paid': pagado_mora,
            'capital_paid': aporte_capital,
            'numero_referencia': self.numero_referencia,
            'saldo_pendiente':saldo_pendiente,
            'description':  descripcion,
            'acreedor': acreedor,
            'seguro':seguro
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
            if credito is not None:
                credito.is_paid_off = True
                credito.saldo_pendiente = 0
                credito.save()

            if acreedor is not None:
                acreedor.is_paid_off = True
                acreedor.saldo_pendiente = 0
                acreedor.save()

            if seguro is not None:
                seguro.is_paid_off = True
                seguro.saldo_pendiente = 0
                seguro.save()
            
            
            logger.error(f'EL CREDITO PAGADO COMPLETAMENTE')
            if siguiente:
                siguiente.delete()

            return f'EL CREDITO PAGADO COMPLETAMENTE'
            
        
        # SE ACTUALIZA EL SALDO PENDIENTE DEL CREDITO
        if credito is not None:
            credito.saldo_pendiente = saldo_pendiente

        if acreedor is not None:
            acreedor.saldo_pendiente = saldo_pendiente

        if seguro is not None:
            seguro.saldo_pendiente = saldo_pendiente
        

        # Actualizar el saldo actual
        if saldo_pendiente <= 0:
            saldo_pendiente = 0

        if credito is not None:
            credito.saldo_actual = saldo_pendiente + cuota.mora + cuota.interest
            credito.save()

        if acreedor is not None:
            acreedor.saldo_actual = saldo_pendiente + cuota.mora + cuota.interest
            acreedor.save()
            
        if seguro is not None:
            seguro.saldo_actual = saldo_pendiente + cuota.mora + cuota.interest
            seguro.save()
        
        


        
        mora = calculo_mora(saldo_pendiente, tasa_interes)
        
       
        
        if siguiente:
            # Actualizamos la siguiente cuota si ya existe
            cuota_a_actualizar = siguiente
            logger.info(f'LA CUOTA: {siguiente}\nREALIZA CAMBIOS SOBRE:\nINTERES ANTIGUO: {cuota_a_actualizar.interest}\nMORA ANTIGUA: {cuota_a_actualizar.mora}\nSALDO PENDIENTE: {cuota_a_actualizar.saldo_pendiente}')
            cuota_a_actualizar.cambios = True
            if cuota.interest <=0:
                cuota_a_actualizar.interest =  interes
                pago.cuota_vencida = False
            else:
                cuota_a_actualizar.interest  = max (0, cuota_a_actualizar.interest - pagado_interes)
            cuota_a_actualizar.mora = Decimal(cuota_a_actualizar.interest) * Decimal(0.1)  
            cuota_a_actualizar.mora_generado = Decimal(cuota_a_actualizar.interest) * Decimal(0.1)
                
        else:
            logger.info('CREACION DE UNA NUEVA  CUOTA')
            
            
                

        # En ambos casos (cuota nueva o existente), actualizamos los campos comunes
        if cuota_a_actualizar:
            cuota_a_actualizar.start_date = cuota.due_date
            cuota_a_actualizar.saldo_pendiente = saldo_pendiente
            cuota_a_actualizar.credit_id = credito
            cuota_a_actualizar.outstanding_balance = saldo_pendiente

            if credito is not None:
                credito.saldo_actual = saldo_pendiente + cuota_a_actualizar.mora + cuota_a_actualizar.interest
                credito.save()

            if acreedor is not None:
                acreedor.saldo_actual = saldo_pendiente + cuota_a_actualizar.mora + cuota_a_actualizar.interest
                acreedor.save()
                
            if seguro is not None:
                seguro.saldo_actual = saldo_pendiente + cuota_a_actualizar.mora + cuota_a_actualizar.interest
                seguro.save()
            
            
            
            logger.info(f'LA CUOTA: {siguiente}\nREALIZA CAMBIOS SOBRE:\nINTERES NUEVO: {cuota_a_actualizar.interest}\nMORA NUEVA: {cuota_a_actualizar.mora}\nSALDO PENDIENTE: {saldo_pendiente}')
            

            # Guardamos los cambios
            #if cuota_a_actualizar:
            cuota_a_actualizar.save()
        

        



    def __str__(self):
        return f'PAGO {self.numero_referencia} - {self.estado_transaccion}'

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'