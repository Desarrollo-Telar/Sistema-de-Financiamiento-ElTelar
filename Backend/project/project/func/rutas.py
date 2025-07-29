import os

commands = [
    "python manage.py dumpdata accountings.Creditor --format=json --indent=4 > modelos/fixtures/Acreedor.json",
    "python manage.py dumpdata accountings.Insurance --format=json --indent=4 > modelos/fixtures/Seguro.json",
    "python manage.py dumpdata accountings.Income --format=json --indent=4 > modelos/fixtures/Ingreso.json",
    "python manage.py dumpdata accountings.Egress --format=json --indent=4 > modelos/fixtures/Gastos.json",
    
    "python manage.py dumpdata addresses.Address --format=json --indent=4 > modelos/fixtures/Direccion.json",
    "python manage.py dumpdata addresses.Departamento --format=json --indent=4 > modelos/fixtures/Departamento.json",
    "python manage.py dumpdata addresses.Municiopio --format=json --indent=4 > modelos/fixtures/Municipio.json",
    
    "python manage.py dumpdata customers.ImmigrationStatus --format=json --indent=4 > modelos/fixtures/CondicionMigratoria.json",
    "python manage.py dumpdata customers.Customer --format=json --indent=4 > modelos/fixtures/Cliente.json",
    
    "python manage.py dumpdata documents.DocumentBank --format=json --indent=4 > modelos/fixtures/DocumentoBanco.json",
    "python manage.py dumpdata documents.Document --format=json --indent=4 > modelos/fixtures/Documento.json",
    "python manage.py dumpdata documents.DocumentCustomer --format=json --indent=4 > modelos/fixtures/DocumentoCliente.json",
    "python manage.py dumpdata documents.DocumentAddress --format=json --indent=4 > modelos/fixtures/DocumentoDireccion.json",
    "python manage.py dumpdata documents.DocumentGuarantee --format=json --indent=4 > modelos/fixtures/DocumentoGarantia.json",
    "python manage.py dumpdata documents.DocumentOther --format=json --indent=4 > modelos/fixtures/OtroDocumento.json",
    
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
    
    "python manage.py dumpdata users.User --format=json --indent=4 > modelos/fixtures/User.json",

    "python manage.py dumpdata roles.role --format=json --indent=4 > modelos/fixtures/Roles.json",
    "python manage.py dumpdata roles.CategoriaPermiso --format=json --indent=4 > modelos/fixtures/CategoriasPermisos.json",
    "python manage.py dumpdata roles.Permiso --format=json --indent=4 > modelos/fixtures/Permisos.json",
    "python manage.py dumpdata users.PermisoUsuario --format=json --indent=4 > modelos/fixtures/PermisosUsuarios.json",
]

load_commands = [
    "python manage.py loaddata modelos/fixtures/Roles.json",
    "python manage.py loaddata modelos/fixtures/CategoriasPermisos.json",
    "python manage.py loaddata modelos/fixtures/Permisos.json",
    "python manage.py loaddata modelos/fixtures/CondicionMigratoria.json",
    "python manage.py loaddata modelos/fixtures/Departamento.json",
    "python manage.py loaddata modelos/fixtures/Municipio.json",

    "python manage.py loaddata modelos/fixtures/User.json",
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

print("PROCESANDO...")
for back in commands:
    os.system(back)
print("FINALIZADO")