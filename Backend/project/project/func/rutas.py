import os

commands = [
    "python manage.py dumpdata accountings.Creditor --format=json --indent=4 > modelos/fixtures/Acreedor.json",
    "python manage.py dumpdata accountings.Insurance --format=json --indent=4 > modelos/fixtures/Seguro.json",
    "python manage.py dumpdata accountings.Income --format=json --indent=4 > modelos/fixtures/Ingreso.json",
    "python manage.py dumpdata accountings.Egress --format=json --indent=4 > modelos/fixtures/Gastos.json",

    "python manage.py dumpdata actividades.Notification --format=json --indent=4 > modelos/fixtures/Notification.json",
    "python manage.py dumpdata actividades.NotificationCustomer --format=json --indent=4 > modelos/fixtures/NotificationCustomer.json",
    "python manage.py dumpdata actividades.DocumentoNotificacionCliente --format=json --indent=4 > modelos/fixtures/DocumentoNotificacionCliente.json",
    "python manage.py dumpdata actividades.UserLog --format=json --indent=4 > modelos/fixtures/UserLog.json",
    "python manage.py dumpdata actividades.SystemLog --format=json --indent=4 > modelos/fixtures/SystemLog.json",
    "python manage.py dumpdata actividades.LogLevel --format=json --indent=4 > modelos/fixtures/LogLevel.json",
    "python manage.py dumpdata actividades.LogCategory --format=json --indent=4 > modelos/fixtures/LogCategory.json",
    "python manage.py dumpdata actividades.Checkpoint --format=json --indent=4 > modelos/fixtures/Checkpoint.json",
    "python manage.py dumpdata actividades.VotacionCliente --format=json --indent=4 > modelos/fixtures/VotacionCliente.json",
    "python manage.py dumpdata actividades.VotacionCredito --format=json --indent=4 > modelos/fixtures/VotacionCredito.json",
    "python manage.py dumpdata actividades.Informe --format=json --indent=4 > modelos/fixtures/Informe.json",
    "python manage.py dumpdata actividades.DetalleInformeCobranza --format=json --indent=4 > modelos/fixtures/DetalleInformeCobranza.json",
    "python manage.py dumpdata actividades.Informe --format=json --indent=4 > modelos/fixtures/Informe.json",
    "python manage.py dumpdata actividades.InformeDiarioSistema --format=json --indent=4 > modelos/fixtures/InformeDiarioSistema.json",
    "python manage.py dumpdata actividades.DetalleInformeDiario --format=json --indent=4 > modelos/fixtures/DetalleInformeDiario.json",
    "python manage.py dumpdata actividades.ModelHistory --format=json --indent=4 > modelos/fixtures/ModelHistory.json",
    
    "python manage.py dumpdata addresses.Address --format=json --indent=4 > modelos/fixtures/Direccion.json",
    "python manage.py dumpdata addresses.Departamento --format=json --indent=4 > modelos/fixtures/Departamento.json",
    "python manage.py dumpdata addresses.Municiopio --format=json --indent=4 > modelos/fixtures/Municipio.json",
    
    "python manage.py dumpdata customers.ImmigrationStatus --format=json --indent=4 > modelos/fixtures/CondicionMigratoria.json",
    "python manage.py dumpdata customers.Customer --format=json --indent=4 > modelos/fixtures/Cliente.json",
    "python manage.py dumpdata customers.Profession --format=json --indent=4 > modelos/fixtures/Profession.json",
    "python manage.py dumpdata customers.Occupation --format=json --indent=4 > modelos/fixtures/Occupation.json",
    "python manage.py dumpdata customers.CreditCounselor --format=json --indent=4 > modelos/fixtures/CreditCounselor.json",
    "python manage.py dumpdata customers.Cobranza --format=json --indent=4 > modelos/fixtures/Cobranza.json",
    "python manage.py dumpdata customers.HistorialCobranza --format=json --indent=4 > modelos/fixtures/HistorialCobranza.json",
    
    "python manage.py dumpdata documents.DocumentBank --format=json --indent=4 > modelos/fixtures/DocumentoBanco.json",
    "python manage.py dumpdata documents.Document --format=json --indent=4 > modelos/fixtures/Documento.json",
    "python manage.py dumpdata documents.DocumentCustomer --format=json --indent=4 > modelos/fixtures/DocumentoCliente.json",
    "python manage.py dumpdata documents.DocumentAddress --format=json --indent=4 > modelos/fixtures/DocumentoDireccion.json",
    "python manage.py dumpdata documents.DocumentGuarantee --format=json --indent=4 > modelos/fixtures/DocumentoGarantia.json",
    "python manage.py dumpdata documents.DocumentOther --format=json --indent=4 > modelos/fixtures/OtroDocumento.json",
    "python manage.py dumpdata documents.DocumentSubsidiary --format=json --indent=4 > modelos/fixtures/DocumentSubsidiary.json",
    
    
    "python manage.py dumpdata FinancialInformation.WorkingInformation --format=json --indent=4 > modelos/fixtures/InformacionLaboral.json",
    "python manage.py dumpdata FinancialInformation.OtherSourcesOfIncome --format=json --indent=4 > modelos/fixtures/OtraInformacionDeIngreso.json",
    "python manage.py dumpdata FinancialInformation.Reference --format=json --indent=4 > modelos/fixtures/Referencia.json",
    
    "python manage.py dumpdata financings.AccountStatement --format=json --indent=4 > modelos/fixtures/EstadoCuenta.json",
    "python manage.py dumpdata financings.Banco --format=json --indent=4 > modelos/fixtures/Banco.json",
    "python manage.py dumpdata financings.Credit --format=json --indent=4 > modelos/fixtures/Credito.json",
    "python manage.py dumpdata financings.Disbursement --format=json --indent=4 > modelos/fixtures/Desembolso.json",
    "python manage.py dumpdata financings.Guarantees --format=json --indent=4 > modelos/fixtures/Garantia.json",
    "python manage.py dumpdata financings.DetailsGuarantees --format=json --indent=4 > modelos/fixtures/DetalleGarantia.json",
    "python manage.py dumpdata financings.Payment --format=json --indent=4 > modelos/fixtures/Boleta.json",
    "python manage.py dumpdata financings.PaymentPlan --format=json --indent=4 > modelos/fixtures/Cuota.json",
    "python manage.py dumpdata financings.Recibo --format=json --indent=4 > modelos/fixtures/Recibo.json",
    "python manage.py dumpdata financings.Invoice --format=json --indent=4 > modelos/fixtures/Factura.json",
    
    "python manage.py dumpdata InvestmentPlan.InvestmentPlan --format=json --indent=4 > modelos/fixtures/Destino.json",
    
    "python manage.py dumpdata pictures.Imagen --format=json --indent=4 > modelos/fixtures/Imagen.json",
    "python manage.py dumpdata pictures.ImagenCustomer --format=json --indent=4 > modelos/fixtures/ImagenCliente.json",
    "python manage.py dumpdata pictures.ImagenAddress --format=json --indent=4 > modelos/fixtures/ImagenDireccion.json",
    "python manage.py dumpdata pictures.ImagenGuarantee --format=json --indent=4 > modelos/fixtures/ImagenGarantia.json",
    "python manage.py dumpdata pictures.ImagenOther --format=json --indent=4 > modelos/fixtures/OtraImagen.json",
    "python manage.py dumpdata pictures.ImagenSubsidiary --format=json --indent=4 > modelos/fixtures/ImagenSubsidiary.json",

    "python manage.py dumpdata subsidiaries.Subsidiary --format=json --indent=4 > modelos/fixtures/Subsidiary.json",
    "python manage.py dumpdata subsidiaries.HorarioSucursal --format=json --indent=4 > modelos/fixtures/HorarioSucursal.json",
    
    "python manage.py dumpdata users.User --format=json --indent=4 > modelos/fixtures/User.json",
    "python manage.py dumpdata users.PermisoUsuario --format=json --indent=4 > modelos/fixtures/PermisosUsuarios.json",

    "python manage.py dumpdata roles.role --format=json --indent=4 > modelos/fixtures/Roles.json",
    "python manage.py dumpdata roles.CategoriaPermiso --format=json --indent=4 > modelos/fixtures/CategoriasPermisos.json",
    "python manage.py dumpdata roles.Permiso --format=json --indent=4 > modelos/fixtures/Permisos.json",
    
]

load_commands = [
    "python manage.py loaddata modelos/fixtures/Roles.json",
    "python manage.py loaddata modelos/fixtures/CategoriasPermisos.json",
    "python manage.py loaddata modelos/fixtures/Permisos.json",
    "python manage.py loaddata modelos/fixtures/CondicionMigratoria.json",
    "python manage.py loaddata modelos/fixtures/Departamento.json",
    "python manage.py loaddata modelos/fixtures/Municipio.json",

    "python manage.py loaddata modelos/fixtures/Subsidiary.json",
    "python manage.py loaddata modelos/fixtures/User.json",
    "python manage.py loaddata modelos/fixtures/CreditCounselor.json",
    "python manage.py loaddata modelos/fixtures/Cliente.json",
    "python manage.py loaddata modelos/fixtures/PermisosUsuarios.json",
    "python manage.py loaddata modelos/fixtures/Direccion.json",

    "python manage.py loaddata modelos/fixtures/Acreedor.json",
    "python manage.py loaddata modelos/fixtures/Seguro.json",
    "python manage.py loaddata modelos/fixtures/Ingreso.json",
    "python manage.py loaddata modelos/fixtures/Gastos.json",
    
    "python manage.py loaddata modelos/fixtures/InformacionLaboral.json",
    "python manage.py loaddata modelos/fixtures/OtraInformacionDeIngreso.json",
    "python manage.py loaddata modelos/fixtures/Referencia.json",
    "python manage.py loaddata modelos/fixtures/Destino.json",
    
    "python manage.py loaddata modelos/fixtures/Credito.json",
    "python manage.py loaddata modelos/fixtures/Cuota.json",
    "python manage.py loaddata modelos/fixtures/Desembolso.json",

    "python manage.py loaddata modelos/fixtures/Banco.json",
    "python manage.py loaddata modelos/fixtures/Boleta.json",
    "python manage.py loaddata modelos/fixtures/Recibo.json",
    "python manage.py loaddata modelos/fixtures/Factura.json",
    
    
    
    "python manage.py loaddata modelos/fixtures/Garantia.json",
    "python manage.py loaddata modelos/fixtures/DetalleGarantia.json",
    "python manage.py loaddata modelos/fixtures/EstadoCuenta.json",
    
    
    
    
    "python manage.py loaddata modelos/fixtures/Imagen.json",
    "python manage.py loaddata modelos/fixtures/ImagenCliente.json",
    "python manage.py loaddata modelos/fixtures/ImagenDireccion.json",
    "python manage.py loaddata modelos/fixtures/ImagenGarantia.json",
    "python manage.py loaddata modelos/fixtures/OtraImagen.json",

    "python manage.py loaddata modelos/fixtures/Documento.json",
    "python manage.py loaddata modelos/fixtures/DocumentoBanco.json",    
    "python manage.py loaddata modelos/fixtures/DocumentoCliente.json",
    "python manage.py loaddata modelos/fixtures/DocumentoDireccion.json",
    "python manage.py loaddata modelos/fixtures/DocumentoGarantia.json",
    "python manage.py loaddata modelos/fixtures/OtroDocumento.json",
    
    
]

if __name__ == '__main__':
    print("PROCESANDO...")
    for back in load_commands:
        os.system(back)
    print("FINALIZADO")