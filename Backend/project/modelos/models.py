# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FinancialinformationOthersourcesofincome(models.Model):
    id = models.BigAutoField(primary_key=True)
    source_of_income = models.CharField(max_length=100)
    nit = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    customer_id = models.ForeignKey('CustomersCustomer', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'FinancialInformation_othersourcesofincome'


class FinancialinformationReference(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    reference_type = models.CharField(max_length=100)
    customer_id = models.ForeignKey('CustomersCustomer', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'FinancialInformation_reference'


class FinancialinformationWorkinginformation(models.Model):
    id = models.BigAutoField(primary_key=True)
    position = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    start_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    working_hours = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=20)
    source_of_income = models.CharField(max_length=90)
    income_detail = models.TextField(blank=True, null=True)
    employment_status = models.CharField(max_length=150)
    customer_id = models.ForeignKey('CustomersCustomer', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'FinancialInformation_workinginformation'


class InvestmentplanInvestmentplan(models.Model):
    id = models.BigAutoField(primary_key=True)
    type_of_product_or_service = models.CharField(max_length=75)
    total_value_of_the_product_or_service = models.DecimalField(max_digits=15, decimal_places=2)
    investment_plan_description = models.TextField(blank=True, null=True)
    initial_amount = models.DecimalField(max_digits=15, decimal_places=2)
    monthly_amount = models.DecimalField(max_digits=15, decimal_places=2)
    transfers_or_transfer_of_funds = models.BooleanField()
    type_of_transfers_or_transfer_of_funds = models.CharField(max_length=75)
    investment_plan_code = models.CharField(unique=True, max_length=25)
    customer_id = models.ForeignKey('CustomersCustomer', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'InvestmentPlan_investmentplan'


class AccountingsCreditor(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo_acreedor = models.CharField(max_length=100)
    nombre_acreedor = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    tasa = models.DecimalField(max_digits=5, decimal_places=3)
    plazo = models.IntegerField()
    fecha_vencimiento = models.DateField()
    fecha_registro = models.DateField()
    numero_referencia = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    boleta = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField()
    saldo_pendiente = models.DecimalField(max_digits=15, decimal_places=2)
    saldo_actual = models.DecimalField(max_digits=15, decimal_places=2)
    is_paid_off = models.BooleanField()
    estado_aportacion = models.BooleanField(blank=True, null=True)
    estados_fechas = models.BooleanField(blank=True, null=True)
    forma_de_pago = models.CharField(max_length=75)
    creation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accountings_creditor'


class AccountingsEgress(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField()
    fecha_doc_fiscal = models.DateField(blank=True, null=True)
    numero_doc = models.CharField(max_length=155, blank=True, null=True)
    nit = models.CharField(max_length=50, blank=True, null=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    monto_doc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    codigo_egreso = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    numero_referencia = models.CharField(unique=True, max_length=255)
    boleta = models.CharField(max_length=100, blank=True, null=True)
    documento = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField()
    fecha_registro = models.DateField()
    nombre = models.CharField(max_length=150, blank=True, null=True)
    pago_correspondiente = models.CharField(max_length=150, blank=True, null=True)
    tipo_impuesto = models.CharField(max_length=150, blank=True, null=True)
    acreedor = models.ForeignKey(AccountingsCreditor, models.DO_NOTHING, blank=True, null=True)
    seguro = models.ForeignKey('AccountingsInsurance', models.DO_NOTHING, blank=True, null=True)
    tipo_gasto = models.CharField(max_length=150, blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accountings_egress'


class AccountingsIncome(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    codigo_ingreso = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    numero_referencia = models.CharField(unique=True, max_length=255)
    boleta = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField()
    fecha_registro = models.DateField()
    creation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accountings_income'


class AccountingsInsurance(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo_seguro = models.CharField(max_length=100)
    nombre_acreedor = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    tasa = models.DecimalField(max_digits=5, decimal_places=3)
    plazo = models.IntegerField()
    fecha_vencimiento = models.DateField()
    fecha_registro = models.DateField()
    numero_referencia = models.CharField(max_length=255)
    observaciones = models.TextField(blank=True, null=True)
    boleta = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField()
    saldo_pendiente = models.DecimalField(max_digits=15, decimal_places=2)
    saldo_actual = models.DecimalField(max_digits=15, decimal_places=2)
    is_paid_off = models.BooleanField()
    estado_aportacion = models.BooleanField(blank=True, null=True)
    estados_fechas = models.BooleanField(blank=True, null=True)
    forma_de_pago = models.CharField(max_length=75)
    credito = models.ForeignKey('FinancingsCredit', models.DO_NOTHING, blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accountings_insurance'


class AddressesAddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    street = models.CharField(max_length=120)
    number = models.CharField(max_length=90)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=90)
    country = models.CharField(max_length=90)
    type_address = models.CharField(max_length=90)
    latitud = models.CharField(max_length=120)
    longitud = models.CharField(max_length=120)
    customer_id = models.ForeignKey('CustomersCustomer', models.DO_NOTHING, blank=True, null=True)
    codigo_postal = models.CharField(max_length=100, blank=True, null=True)
    subsidiary = models.ForeignKey('SubsidiariesSubsidiary', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses_address'


class AddressesDepartamento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    codigo_postal = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses_departamento'


class AddressesMuniciopio(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=120)
    depart = models.ForeignKey(AddressesDepartamento, models.DO_NOTHING)
    codigo_postal = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses_municiopio'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class CodesCode(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.CharField(max_length=5)
    user = models.OneToOneField('UsersUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'codes_code'


class CustomersCustomer(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_code = models.CharField(unique=True, max_length=25)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    type_identification = models.CharField(max_length=50)
    identification_number = models.CharField(unique=True, max_length=15)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=254)
    status = models.CharField(max_length=75)
    date_birth = models.DateField()
    number_nit = models.CharField(unique=True, max_length=20)
    place_birth = models.CharField(max_length=75)
    marital_status = models.CharField(max_length=50)
    profession_trade = models.CharField(max_length=75, blank=True, null=True)
    gender = models.CharField(max_length=50)
    nationality = models.CharField(max_length=75)
    person_type = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField()
    asesor = models.CharField(max_length=100, blank=True, null=True)
    fehca_vencimiento_de_tipo_identificacion = models.DateField(blank=True, null=True)
    user_id = models.ForeignKey('UsersUser', models.DO_NOTHING, blank=True, null=True)
    immigration_status_id = models.ForeignKey('CustomersImmigrationstatus', models.DO_NOTHING, blank=True, null=True)
    level_of_education = models.CharField(max_length=100, blank=True, null=True)
    level_of_education_superior = models.CharField(max_length=100, blank=True, null=True)
    other_telephone = models.CharField(max_length=20, blank=True, null=True)
    ocupacion = models.ForeignKey('CustomersOccupation', models.DO_NOTHING, blank=True, null=True)
    profesion = models.ForeignKey('CustomersProfession', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers_customer'


class CustomersImmigrationstatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    condition_name = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers_immigrationstatus'


class CustomersOccupation(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo_ocupacion = models.CharField(max_length=100)
    nombre = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'customers_occupation'


class CustomersProfession(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo_profesion = models.CharField(max_length=100)
    nombre = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'customers_profession'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsersUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCeleryBeatClockedschedule(models.Model):
    clocked_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_clockedschedule'


class DjangoCeleryBeatCrontabschedule(models.Model):
    minute = models.CharField(max_length=240)
    hour = models.CharField(max_length=96)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=124)
    month_of_year = models.CharField(max_length=64)
    timezone = models.CharField(max_length=63)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_crontabschedule'


class DjangoCeleryBeatIntervalschedule(models.Model):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_intervalschedule'


class DjangoCeleryBeatPeriodictask(models.Model):
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    routing_key = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.BooleanField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.IntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()
    crontab = models.ForeignKey(DjangoCeleryBeatCrontabschedule, models.DO_NOTHING, blank=True, null=True)
    interval = models.ForeignKey(DjangoCeleryBeatIntervalschedule, models.DO_NOTHING, blank=True, null=True)
    solar = models.ForeignKey('DjangoCeleryBeatSolarschedule', models.DO_NOTHING, blank=True, null=True)
    one_off = models.BooleanField()
    start_time = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    headers = models.TextField()
    clocked = models.ForeignKey(DjangoCeleryBeatClockedschedule, models.DO_NOTHING, blank=True, null=True)
    expire_seconds = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictask'


class DjangoCeleryBeatPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictasks'


class DjangoCeleryBeatSolarschedule(models.Model):
    event = models.CharField(max_length=24)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_solarschedule'
        unique_together = (('event', 'latitude', 'longitude'),)


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class DocumentsDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    document = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'documents_document'


class DocumentsDocumentaddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    address_id = models.ForeignKey(AddressesAddress, models.DO_NOTHING)
    customer_id = models.ForeignKey(CustomersCustomer, models.DO_NOTHING)
    document_id = models.ForeignKey(DocumentsDocument, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'documents_documentaddress'


class DocumentsDocumentbank(models.Model):
    id = models.BigAutoField(primary_key=True)
    document = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'documents_documentbank'


class DocumentsDocumentcustomer(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_id = models.ForeignKey(CustomersCustomer, models.DO_NOTHING)
    document_id = models.ForeignKey(DocumentsDocument, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'documents_documentcustomer'


class DocumentsDocumentguarantee(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_id = models.ForeignKey(CustomersCustomer, models.DO_NOTHING, blank=True, null=True)
    document_id = models.ForeignKey(DocumentsDocument, models.DO_NOTHING)
    garantia = models.ForeignKey('FinancingsDetailsguarantees', models.DO_NOTHING, blank=True, null=True)
    investment_plan_id = models.ForeignKey(InvestmentplanInvestmentplan, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents_documentguarantee'


class DocumentsDocumentother(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    customer_id = models.ForeignKey(CustomersCustomer, models.DO_NOTHING)
    document_id = models.ForeignKey(DocumentsDocument, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'documents_documentother'


class DocumentsDocumentsubsidiary(models.Model):
    id = models.BigAutoField(primary_key=True)
    ddescription = models.TextField(blank=True, null=True)
    document = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField()
    subsidiary = models.ForeignKey('SubsidiariesSubsidiary', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'documents_documentsubsidiary'


class FinancingsAccountstatement(models.Model):
    id = models.BigAutoField(primary_key=True)
    issue_date = models.DateField()
    disbursement_paid = models.DecimalField(max_digits=10, decimal_places=2)
    interest_paid = models.DecimalField(max_digits=10, decimal_places=2)
    capital_paid = models.DecimalField(max_digits=10, decimal_places=2)
    late_fee_paid = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2)
    abono = models.DecimalField(max_digits=12, decimal_places=2)
    numero_referencia = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    credit = models.ForeignKey('FinancingsCredit', models.DO_NOTHING, blank=True, null=True)
    disbursement = models.ForeignKey('FinancingsDisbursement', models.DO_NOTHING, blank=True, null=True)
    payment = models.ForeignKey('FinancingsPayment', models.DO_NOTHING, blank=True, null=True)
    cuota = models.ForeignKey('FinancingsPaymentplan', models.DO_NOTHING, blank=True, null=True)
    acreedor = models.ForeignKey(AccountingsCreditor, models.DO_NOTHING, blank=True, null=True)
    seguro = models.ForeignKey(AccountingsInsurance, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'financings_accountstatement'


class FinancingsBanco(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField()
    referencia = models.CharField(unique=True, max_length=100)
    credito = models.DecimalField(max_digits=12, decimal_places=2)
    debito = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField()
    status = models.BooleanField()
    secuencial = models.CharField(max_length=100)
    cheque = models.CharField(max_length=100)
    saldo_contable = models.DecimalField(max_digits=12, decimal_places=2)
    saldo_disponible = models.DecimalField(max_digits=12, decimal_places=2)
    registro_ficticio = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'financings_banco'


class FinancingsCredit(models.Model):
    id = models.BigAutoField(primary_key=True)
    proposito = models.TextField()
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    plazo = models.IntegerField()
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=3)
    forma_de_pago = models.CharField(max_length=75)
    frecuencia_pago = models.CharField(max_length=75)
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    tipo_credito = models.CharField(max_length=75)
    codigo_credito = models.CharField(max_length=25, blank=True, null=True)
    creation_date = models.DateTimeField()
    is_paid_off = models.BooleanField()
    tasa_mora = models.DecimalField(max_digits=15, decimal_places=2)
    saldo_pendiente = models.DecimalField(max_digits=15, decimal_places=2)
    saldo_actual = models.DecimalField(max_digits=15, decimal_places=2)
    estado_aportacion = models.BooleanField(blank=True, null=True)
    estados_fechas = models.BooleanField(blank=True, null=True)
    desembolsado_completo = models.BooleanField()
    plazo_restante = models.IntegerField(blank=True, null=True)
    customer_id = models.ForeignKey(CustomersCustomer, models.DO_NOTHING)
    destino_id = models.ForeignKey(InvestmentplanInvestmentplan, models.DO_NOTHING, blank=True, null=True)
    modifico = models.BooleanField()
    numero_credito = models.CharField(max_length=100, blank=True, null=True)
    saldo_sin_modificar = models.DecimalField(max_digits=15, decimal_places=2)
    sucursal = models.ForeignKey('SubsidiariesSubsidiary', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'financings_credit'


class FinancingsCuota(models.Model):
    id = models.BigAutoField(primary_key=True)
    mes = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField(blank=True, null=True)
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2)
    mora = models.DecimalField(max_digits=12, decimal_places=2)
    interest = models.DecimalField(max_digits=12, decimal_places=2)
    principal = models.DecimalField(max_digits=12, decimal_places=2)
    installment = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.BooleanField()
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2)
    interes_pagado = models.DecimalField(max_digits=12, decimal_places=2)
    mora_pagado = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_limite = models.DateTimeField(blank=True, null=True)
    cambios = models.BooleanField()
    numero_referencia = models.CharField(max_length=255, blank=True, null=True)
    cuota_vencida = models.BooleanField()
    credit_id = models.ForeignKey(FinancingsCredit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'financings_cuota'


class FinancingsDetailsguarantees(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo_garantia = models.CharField(max_length=75)
    especificaciones = models.JSONField()
    valor_cobertura = models.DecimalField(max_digits=15, decimal_places=2)
    garantia_id = models.ForeignKey('FinancingsGuarantees', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'financings_detailsguarantees'


class FinancingsDisbursement(models.Model):
    id = models.BigAutoField(primary_key=True)
    forma_desembolso = models.CharField(max_length=75)
    monto_credito = models.DecimalField(max_digits=15, decimal_places=2)
    monto_credito_agregar = models.DecimalField(max_digits=15, decimal_places=2)
    monto_credito_cancelar = models.DecimalField(max_digits=15, decimal_places=2)
    saldo_anterior = models.DecimalField(max_digits=15, decimal_places=2)
    honorarios = models.DecimalField(max_digits=15, decimal_places=2)
    poliza_seguro = models.DecimalField(max_digits=15, decimal_places=2)
    monto_desembolsado = models.DecimalField(max_digits=15, decimal_places=2)
    total_gastos = models.DecimalField(max_digits=15, decimal_places=2)
    monto_total_desembolso = models.DecimalField(max_digits=15, decimal_places=2)
    total_t = models.DecimalField(max_digits=15, decimal_places=2)
    credit_id = models.ForeignKey(FinancingsCredit, models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'financings_disbursement'


class FinancingsGuarantees(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.TextField()
    suma_total = models.DecimalField(max_digits=15, decimal_places=2)
    credit_id = models.ForeignKey(FinancingsCredit, models.DO_NOTHING)
    abogado = models.CharField(max_length=100, blank=True, null=True)
    tipo_contrado = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'financings_guarantees'


class FinancingsInvoice(models.Model):
    id = models.BigAutoField(primary_key=True)
    issue_date = models.DateField()
    numero_factura = models.IntegerField()
    recibo_id = models.ForeignKey('FinancingsRecibo', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'financings_invoice'


class FinancingsPayment(models.Model):
    id = models.BigAutoField(primary_key=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    numero_referencia = models.CharField(unique=True, max_length=255)
    fecha_emision = models.DateTimeField()
    fecha_creacion = models.DateTimeField()
    estado_transaccion = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True, null=True)
    mora = models.DecimalField(max_digits=12, decimal_places=2)
    interes = models.DecimalField(max_digits=12, decimal_places=2)
    interes_generado = models.DecimalField(max_digits=12, decimal_places=2)
    capital = models.DecimalField(max_digits=12, decimal_places=2)
    capital_generado = models.DecimalField(max_digits=12, decimal_places=2)
    boleta = models.CharField(max_length=100, blank=True, null=True)
    tipo_pago = models.CharField(max_length=75)
    descripcion_estado = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField()
    credit = models.ForeignKey(FinancingsCredit, models.DO_NOTHING, blank=True, null=True)
    disbursement = models.ForeignKey(FinancingsDisbursement, models.DO_NOTHING, blank=True, null=True)
    cliente = models.ForeignKey(CustomersCustomer, models.DO_NOTHING, blank=True, null=True)
    acreedor = models.ForeignKey(AccountingsCreditor, models.DO_NOTHING, blank=True, null=True)
    seguro = models.ForeignKey(AccountingsInsurance, models.DO_NOTHING, blank=True, null=True)
    registro_ficticio = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'financings_payment'


class FinancingsPaymentplan(models.Model):
    id = models.BigAutoField(primary_key=True)
    mes = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField(blank=True, null=True)
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2)
    mora = models.DecimalField(max_digits=12, decimal_places=2)
    interest = models.DecimalField(max_digits=12, decimal_places=2)
    principal = models.DecimalField(max_digits=12, decimal_places=2)
    principal_pagado = models.DecimalField(max_digits=12, decimal_places=2)
    installment = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.BooleanField()
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2)
    interes_pagado = models.DecimalField(max_digits=12, decimal_places=2)
    mora_pagado = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_limite = models.DateTimeField(blank=True, null=True)
    cambios = models.BooleanField()
    numero_referencia = models.CharField(max_length=255, blank=True, null=True)
    cuota_vencida = models.BooleanField()
    interes_generado = models.DecimalField(max_digits=12, decimal_places=2)
    capital_generado = models.DecimalField(max_digits=12, decimal_places=2)
    interes_acumulado_generado = models.DecimalField(max_digits=12, decimal_places=2)
    mora_acumulado_generado = models.DecimalField(max_digits=12, decimal_places=2)
    mora_generado = models.DecimalField(max_digits=12, decimal_places=2)
    paso_por_task = models.BooleanField()
    credit_id = models.ForeignKey(FinancingsCredit, models.DO_NOTHING, blank=True, null=True)
    acreedor = models.ForeignKey(AccountingsCreditor, models.DO_NOTHING, blank=True, null=True)
    seguro = models.ForeignKey(AccountingsInsurance, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'financings_paymentplan'


class FinancingsRecibo(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField()
    recibo = models.IntegerField()
    interes = models.DecimalField(max_digits=12, decimal_places=2)
    interes_pagado = models.DecimalField(max_digits=12, decimal_places=2)
    mora = models.DecimalField(max_digits=12, decimal_places=2)
    mora_pagada = models.DecimalField(max_digits=12, decimal_places=2)
    aporte_capital = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    factura = models.BooleanField()
    cliente = models.ForeignKey(CustomersCustomer, models.DO_NOTHING, blank=True, null=True)
    cuota = models.ForeignKey(FinancingsPaymentplan, models.DO_NOTHING, blank=True, null=True)
    pago = models.ForeignKey(FinancingsPayment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'financings_recibo'


class PicturesImagen(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pictures_imagen'


class PicturesImagenaddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    address_id = models.ForeignKey(AddressesAddress, models.DO_NOTHING)
    customer_id = models.ForeignKey(CustomersCustomer, models.DO_NOTHING)
    image_id = models.ForeignKey(PicturesImagen, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pictures_imagenaddress'


class PicturesImagencustomer(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_id = models.ForeignKey(CustomersCustomer, models.DO_NOTHING)
    image_id = models.ForeignKey(PicturesImagen, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pictures_imagencustomer'


class PicturesImagenguarantee(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_id = models.ForeignKey(CustomersCustomer, models.DO_NOTHING)
    image_id = models.ForeignKey(PicturesImagen, models.DO_NOTHING)
    investment_plan_id = models.ForeignKey(InvestmentplanInvestmentplan, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pictures_imagenguarantee'


class PicturesImagenother(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    customer_id = models.ForeignKey(CustomersCustomer, models.DO_NOTHING)
    image_id = models.ForeignKey(PicturesImagen, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pictures_imagenother'


class PicturesImagensubsidiary(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField()
    subsidiary = models.ForeignKey('SubsidiariesSubsidiary', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pictures_imagensubsidiary'


class RatingsRating(models.Model):
    id = models.BigAutoField(primary_key=True)
    calificacion = models.CharField(max_length=75)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField()
    cliente = models.ForeignKey(CustomersCustomer, models.DO_NOTHING)
    usuario = models.ForeignKey('UsersUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ratings_rating'


class RolesRole(models.Model):
    id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles_role'


class RolesRolePermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(RolesRole, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'roles_role_permissions'
        unique_together = (('role', 'permission'),)


class RolesUserrole(models.Model):
    id = models.BigAutoField(primary_key=True)
    idrole = models.ForeignKey(RolesRole, models.DO_NOTHING, db_column='idRole_id')  # Field name made lowercase.
    iduser = models.ForeignKey('UsersUser', models.DO_NOTHING, db_column='idUser_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'roles_userrole'


class SubsidiariesHorariosucursal(models.Model):
    id = models.BigAutoField(primary_key=True)
    dia = models.CharField(max_length=10)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    activo = models.BooleanField()
    sucursal = models.ForeignKey('SubsidiariesSubsidiary', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'subsidiaries_horariosucursal'
        unique_together = (('sucursal', 'dia'),)


class SubsidiariesSubsidiary(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo_sucursal = models.CharField(max_length=100, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    fecha_apertura = models.DateField()
    numero_telefono = models.CharField(max_length=100, blank=True, null=True)
    otro_numero_telefono = models.CharField(max_length=100, blank=True, null=True)
    activa = models.BooleanField()
    codigo_postal = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subsidiaries_subsidiary'


class UsersUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    type_identification = models.CharField(max_length=50)
    identification_number = models.CharField(unique=True, max_length=15)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(unique=True, max_length=254)
    status = models.BooleanField()
    gender = models.CharField(max_length=50)
    user_code = models.CharField(unique=True, max_length=25)
    nationality = models.CharField(max_length=75)
    profile_pic = models.CharField(max_length=100, blank=True, null=True)
    rol = models.CharField(max_length=50)
    creation_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users_user'


class UsersUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UsersUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_user_groups'
        unique_together = (('user', 'group'),)


class UsersUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UsersUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_user_user_permissions'
        unique_together = (('user', 'permission'),)
