@echo off
:: Cambia los valores según tu usuario, contraseña y ruta del programa
set "usuario=AdministradorLocal"
set "contrasena=TuContrasena"
set "programa=C:\ruta\a\aplicacion.exe"

:: Ejecuta el programa con las credenciales
echo Ejecutando como administrador...
echo %contrasena% | runas /user:%usuario% "%programa%"
pause
