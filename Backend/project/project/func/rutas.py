import os

commands = [
    "python manage.py dumpdata accountings.Creditor --format=json --indent=4 > apps/customers/fixtures/Acreedor.json",
    "python manage.py dumpdata accountings.Insurance --format=json --indent=4 > apps/customers/fixtures/Seguro.json",
    "python manage.py dumpdata accountings.Income --format=json --indent=4 > apps/customers/fixtures/Ingreso.json",
    "python manage.py dumpdata accountings.Egress --format=json --indent=4 > apps/customers/fixtures/Gastos.json",
    
    "python manage.py dumpdata addresses.Address --format=json --indent=4 > apps/customers/fixtures/Direccion.json",
    "python manage.py dumpdata addresses.Departamento --format=json --indent=4 > apps/customers/fixtures/Departamento.json",
    "python manage.py dumpdata addresses.Municiopio --format=json --indent=4 > apps/customers/fixtures/Municipio.json",
    
    "python manage.py dumpdata customers.ImmigrationStatus --format=json --indent=4 > apps/customers/fixtures/CondicionMigratoria.json",
    "python manage.py dumpdata customers.Customer --format=json --indent=4 > apps/customers/fixtures/Cliente.json",
    
    "python manage.py dumpdata documents.DocumentBank --format=json --indent=4 > apps/customers/fixtures/DocumentoBanco.json",
    "python manage.py dumpdata documents.Document --format=json --indent=4 > apps/customers/fixtures/Documento.json",
    "python manage.py dumpdata documents.DocumentCustomer --format=json --indent=4 > apps/customers/fixtures/DocumentoCliente.json",
    "python manage.py dumpdata documents.DocumentAddress --format=json --indent=4 > apps/customers/fixtures/DocumentoDireccion.json",
    "python manage.py dumpdata documents.DocumentGuarantee --format=json --indent=4 > apps/customers/fixtures/DocumentoGarantia.json",
    "python manage.py dumpdata documents.DocumentOther --format=json --indent=4 > apps/customers/fixtures/OtroDocumento.json",
    
    "python manage.py dumpdata FinancialInformation.WorkingInformation --format=json --indent=4 > apps/customers/fixtures/InformacionLaboral.json",
    "python manage.py dumpdata FinancialInformation.OtherSourcesOfIncome --format=json --indent=4 > apps/customers/fixtures/OtraInformacionDeIngreso.json",
    "python manage.py dumpdata FinancialInformation.Reference --format=json --indent=4 > apps/customers/fixtures/Referencia.json",
    
    "python manage.py dumpdata financings.AccountStatement --format=json --indent=4 > apps/customers/fixtures/EstadoCuenta.json",
    "python manage.py dumpdata financings.Banco --format=json --indent=4 > apps/customers/fixtures/Banco.json",
    "python manage.py dumpdata financings.Credit --format=json --indent=4 > apps/customers/fixtures/Credito.json",
    "python manage.py dumpdata financings.Disbursement --format=json --indent=4 > apps/customers/fixtures/Desembolso.json",
    "python manage.py dumpdata financings.Guarantees --format=json --indent=4 > apps/customers/fixtures/Garantia.json",
    "python manage.py dumpdata financings.DetailsGuarantees --format=json --indent=4 > apps/customers/fixtures/DetalleGarantia.json",
    "python manage.py dumpdata financings.Payment --format=json --indent=4 > apps/customers/fixtures/Boleta.json",
    "python manage.py dumpdata financings.PaymentPlan --format=json --indent=4 > apps/customers/fixtures/Cuota.json",
    "python manage.py dumpdata financings.Recibo --format=json --indent=4 > apps/customers/fixtures/Recibo.json",
    "python manage.py dumpdata financings.Invoice --format=json --indent=4 > apps/customers/fixtures/Factura.json",
    
    "python manage.py dumpdata InvestmentPlan.InvestmentPlan --format=json --indent=4 > apps/customers/fixtures/Destino.json",
    
    "python manage.py dumpdata pictures.Imagen --format=json --indent=4 > apps/customers/fixtures/Imagen.json",
    "python manage.py dumpdata pictures.ImagenCustomer --format=json --indent=4 > apps/customers/fixtures/ImagenCliente.json",
    "python manage.py dumpdata pictures.ImagenAddress --format=json --indent=4 > apps/customers/fixtures/ImagenDireccion.json",
    "python manage.py dumpdata pictures.ImagenGuarantee --format=json --indent=4 > apps/customers/fixtures/ImagenGarantia.json",
    "python manage.py dumpdata pictures.ImagenOther --format=json --indent=4 > apps/customers/fixtures/OtraImagen.json",
    
    "python manage.py dumpdata users.User --format=json --indent=4 > apps/customers/fixtures/User.json",

    "python manage.py dumpdata roles.role --format=json --indent=4 > modelos/fixtures/Roles.json",
    "python manage.py dumpdata roles.CategoriaPermiso --format=json --indent=4 > modelos/fixtures/CategoriasPermisos.json",
    "python manage.py dumpdata roles.Permiso --format=json --indent=4 > modelos/fixtures/Permisos.json",
    "python manage.py dumpdata users.PermisoUsuario --format=json --indent=4 > modelos/fixtures/PermisosUsuarios.json",
]

load_commands = [
    "python manage.py loaddata modelos/fixtures/Roles.json",
    "python manage.py loaddata modelos/fixtures/CategoriasPermisos.json",
    "python manage.py loaddata modelos/fixtures/Permisos.json",
    "python manage.py loaddata apps/customers/fixtures/CondicionMigratoria.json",
    "python manage.py loaddata apps/customers/fixtures/Departamento.json",
    "python manage.py loaddata apps/customers/fixtures/Municipio.json",

    "python manage.py loaddata apps/customers/fixtures/User.json",
    "python manage.py loaddata apps/customers/fixtures/Cliente.json",
    "python manage.py loaddata modelos/fixtures/PermisosUsuarios.json",
    "python manage.py loaddata apps/customers/fixtures/Direccion.json",

    "python manage.py loaddata apps/customers/fixtures/Acreedor.json",
    "python manage.py loaddata apps/customers/fixtures/Seguro.json",
    "python manage.py loaddata apps/customers/fixtures/Ingreso.json",
    "python manage.py loaddata apps/customers/fixtures/Gastos.json",
    
    "python manage.py loaddata apps/customers/fixtures/InformacionLaboral.json",
    "python manage.py loaddata apps/customers/fixtures/OtraInformacionDeIngreso.json",
    "python manage.py loaddata apps/customers/fixtures/Referencia.json",
    "python manage.py loaddata apps/customers/fixtures/Destino.json",
    
    "python manage.py loaddata apps/customers/fixtures/Credito.json",
    "python manage.py loaddata apps/customers/fixtures/Cuota.json",
    "python manage.py loaddata apps/customers/fixtures/Desembolso.json",

    "python manage.py loaddata apps/customers/fixtures/Banco.json",
    "python manage.py loaddata apps/customers/fixtures/Boleta.json",
    "python manage.py loaddata apps/customers/fixtures/Recibo.json",
    "python manage.py loaddata apps/customers/fixtures/Factura.json",
    
    
    
    "python manage.py loaddata apps/customers/fixtures/Garantia.json",
    "python manage.py loaddata apps/customers/fixtures/DetalleGarantia.json",
    "python manage.py loaddata apps/customers/fixtures/EstadoCuenta.json",
    
    
    
    
    "python manage.py loaddata apps/customers/fixtures/Imagen.json",
    "python manage.py loaddata apps/customers/fixtures/ImagenCliente.json",
    "python manage.py loaddata apps/customers/fixtures/ImagenDireccion.json",
    "python manage.py loaddata apps/customers/fixtures/ImagenGarantia.json",
    "python manage.py loaddata apps/customers/fixtures/OtraImagen.json",

    "python manage.py loaddata apps/customers/fixtures/Documento.json",
    "python manage.py loaddata apps/customers/fixtures/DocumentoBanco.json",    
    "python manage.py loaddata apps/customers/fixtures/DocumentoCliente.json",
    "python manage.py loaddata apps/customers/fixtures/DocumentoDireccion.json",
    "python manage.py loaddata apps/customers/fixtures/DocumentoGarantia.json",
    "python manage.py loaddata apps/customers/fixtures/OtroDocumento.json",
    
    
]

print("PROCESANDO...")
for back in commands:
    os.system(back)
print("FINALIZADO")