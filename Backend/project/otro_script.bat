<<<<<<< HEAD


@echo off
echo Inciando Programa
powershell -Command "Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe' -Verb runAs"
pause
=======
@echo off
:: Cambia los valores según tu usuario, contraseña y ruta del programa
set "usuario=AdministradorLocal"
set "contrasena=TuContrasena"
set "programa=C:\ruta\a\aplicacion.exe"

:: Ejecuta el programa con las credenciales
echo Ejecutando como administrador...
echo %contrasena% | runas /user:%usuario% "%programa%"
pause
>>>>>>> a2c22a6b2622e8621633cba59e280c3fb991a74a
