# Generated by Django 5.0.4 on 2024-09-24 14:16

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('InvestmentPlan', '0001_initial'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('referencia', models.CharField(max_length=100, unique=True, verbose_name='No.Referencia')),
                ('credito', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Monto')),
                ('debito', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Debito')),
            ],
            options={
                'verbose_name': 'Banco',
                'verbose_name_plural': 'Bancos',
            },
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=150, null=True, verbose_name='Mensaje')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Cliente', to='customers.customer')),
            ],
            options={
                'verbose_name': 'Alerta',
                'verbose_name_plural': 'Alertas',
            },
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposito', models.TextField(verbose_name='Proposito')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Monto')),
                ('plazo', models.IntegerField(verbose_name='Plazo')),
                ('tasa_interes', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Tasa de Interes')),
                ('forma_de_pago', models.CharField(choices=[('NIVELADA', 'NIVELADA'), ('AMORTIZACIONES A CAPITAL', 'AMORTIZACIONES A CAPITAL')], default='NIVELADA', max_length=75, verbose_name='Forma de Pago')),
                ('frecuencia_pago', models.CharField(choices=[('MENSUAL', 'MENSUAL'), ('TRIMESTRAL', 'TRIMESTRAL'), ('SEMANAL', 'SEMANAL')], default='MENSUAL', max_length=75, verbose_name='Frecuencia de Pago')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de Inicio')),
                ('fecha_vencimiento', models.DateField(verbose_name='Fecha de Vencimiento')),
                ('tipo_credito', models.CharField(choices=[('AGROPECUARIO Y/O PRODUCTIVO', 'AGROPECUARIO Y/O PRODUCTIVO'), ('COMERCIO', 'COMERCIO'), ('SERVICIOS', 'SERVICIOS'), ('CONSUMO', 'CONSUMO'), ('VIVIENDA', 'VIVIENDA')], max_length=75, verbose_name='Tipo de Credito')),
                ('codigo_credito', models.CharField(blank=True, max_length=25, null=True, verbose_name='Codigo Credito')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('is_paid_off', models.BooleanField(default=False)),
                ('tasa_mora', models.DecimalField(decimal_places=2, default=0.1, max_digits=15, verbose_name='Tasa de Morosidad')),
                ('saldo_pendiente', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Saldo Pendiente')),
                ('saldo_actual', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Saldo Actual')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer', verbose_name='Cliente')),
                ('destino_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='InvestmentPlan.investmentplan', verbose_name='Destino')),
            ],
            options={
                'verbose_name': 'Credito',
                'verbose_name_plural': 'Creditos',
            },
        ),
        migrations.CreateModel(
            name='Disbursement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forma_desembolso', models.CharField(choices=[('APLICACIÓN GASTOS', 'APLICACIÓN GASTOS'), ('APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE', 'APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE'), ('CANCELACIÓN DE CRÉDITO VIGENTE', 'CANCELACIÓN DE CRÉDITO VIGENTE')], max_length=75, verbose_name='Forma de Desembolso')),
                ('monto_credito', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Monto Credito')),
                ('saldo_anterior', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Saldo Anterior')),
                ('honorarios', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Honorarios')),
                ('poliza_seguro', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Poliza de Seguro')),
                ('monto_total_desembolso', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Monto Total a Desembolsar')),
                ('credit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financings.credit', verbose_name='Credito')),
            ],
            options={
                'verbose_name': 'Desembolso',
                'verbose_name_plural': 'Desembolsos',
            },
        ),
        migrations.CreateModel(
            name='Guarantees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(verbose_name='Descripcion')),
                ('suma_total', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Suma Total de Garantia')),
                ('credit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financings.credit', verbose_name='Credito')),
            ],
            options={
                'verbose_name': 'Garantia',
                'verbose_name_plural': 'Garantias',
            },
        ),
        migrations.CreateModel(
            name='DetailsGuarantees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_garantia', models.CharField(choices=[('HIPOTECA', 'HIPOTECA'), ('DERECHO DE POSESION HIPOTECA', 'DERECHO DE POSESION HIPOTECA'), ('FIADOR', 'FIADOR'), ('CHEQUE', 'CHEQUE'), ('VEHICULO', 'VEHICULO'), ('MOBILIARIA', 'MOBILIARIA')], max_length=75, verbose_name='Tipo de Garantia')),
                ('especificaciones', models.JSONField(verbose_name='Especificaciones')),
                ('valor_cobertura', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valor de Cobertura')),
                ('garantia_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financings.guarantees', verbose_name='Garantia')),
            ],
            options={
                'verbose_name': 'Detalle de Garantia',
                'verbose_name_plural': 'Detalles de Garantias',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Monto')),
                ('numero_referencia', models.CharField(max_length=255, verbose_name='Numero de Referencia')),
                ('fecha_emision', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Emision')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('estado_transaccion', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('COMPLETADO', 'Completado'), ('FALLIDO', 'Fallido')], default='PENDIENTE', max_length=20)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('mora', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('interes', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('capital', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('boleta', models.FileField(blank=True, null=True, upload_to='pagos/boletas/', verbose_name='Boleta')),
                ('tipo_pago', models.CharField(choices=[('DESEMBOLSO', 'DESEMBOLSO'), ('CREDITO', 'CREDITO')], default='CREDITO', max_length=75, verbose_name='Tipo de Pago')),
                ('credit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financings.credit', verbose_name='Credito')),
            ],
        ),
        migrations.CreateModel(
            name='AccountStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(default=django.utils.timezone.now)),
                ('disbursement_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Desembolso Pagado')),
                ('interest_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Interes Pagado')),
                ('capital_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Capital Pagada')),
                ('late_fee_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Mora Pagada')),
                ('saldo_pendiente', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Saldo Pendiente')),
                ('abono', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Abono')),
                ('numero_referencia', models.CharField(max_length=255, verbose_name='Numero de Referencia')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripcion')),
                ('credit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_statements', to='financings.credit')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_statement', to='financings.payment')),
            ],
            options={
                'verbose_name': 'Estado de Cuenta',
                'verbose_name_plural': 'Estados de Cuentas',
            },
        ),
        migrations.CreateModel(
            name='PaymentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.IntegerField(blank=True, default=1, null=True, verbose_name='No.Mes')),
                ('start_date', models.DateTimeField(verbose_name='Fecha de Inicio')),
                ('due_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Vencimiento')),
                ('outstanding_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Monto Prestado')),
                ('mora', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Mora')),
                ('interest', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('principal', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Capital')),
                ('installment', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Cuota')),
                ('status', models.BooleanField(default=False)),
                ('saldo_pendiente', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Saldo Pendiente')),
                ('interes_pagado', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Interes Pagado')),
                ('mora_pagado', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Mora Pagada')),
                ('interes_acumulado', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Interes Acumulada')),
                ('mora_acumulada', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Mora Acumulada')),
                ('interes_acumulado_pagado', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Interes Acumulado Pagado')),
                ('mora_acumulado_pagado', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Mora Acumulado Pagada')),
                ('credit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financings.credit')),
            ],
            options={
                'verbose_name': 'Plan de Pago',
                'verbose_name_plural': 'Planes de Pago',
            },
        ),
        migrations.CreateModel(
            name='Recibo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha De Recibo')),
                ('recibo', models.IntegerField(default=0, verbose_name='No. Recibo')),
                ('interes', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Interes')),
                ('interes_pagado', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('mora', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('mora_pagada', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('aporte_capital', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer', verbose_name='Customer')),
                ('pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financings.payment', verbose_name='Pago')),
            ],
        ),
    ]