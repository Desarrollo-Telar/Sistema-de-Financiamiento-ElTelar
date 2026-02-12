

document.getElementById('creditForm').addEventListener('submit', function (e) {
    e.preventDefault();
    

    // Remover errores previos
    document.querySelectorAll('.form-group').forEach(group => {
        group.classList.remove('error');
    });

    let isValid = true;

    // Validar campos requeridos
    const requiredFields = this.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.closest('.form-group').classList.add('error');
            isValid = false;
        }
    });

    // Validar valores numéricos positivos
    const numericFields = ['id_monto', 'id_plazo', 'id_tasa_interes', 'id_saldo_pendiente', 'id_mora', 'id_interest'];
    numericFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (parseFloat(field.value) < 0) {
            field.closest('.form-group').classList.add('error');
            isValid = false;
        }
    });

    const id_tasa_interes = document.getElementById('id_tasa_interes');

    

    

    if (isValid) {
        // En lugar de enviar, pedimos el código
        confirmarCodigoYEnviar(this);
    } else {
        const firstError = document.querySelector('.form-group.error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
});



async function confirmarCodigoYEnviar(formElement) {
    Swal.fire({
        title: 'Autorización Requerida',
        text: "Ingrese el código de seguridad enviado al administrador:",
        input: 'password',
        inputAttributes: {
            autocapitalize: 'off',
            autocorrect: 'off'
        },
        showCancelButton: true,
        confirmButtonText: 'Verificar y Guardar',
        confirmButtonColor: '#28a745',
        cancelButtonText: 'Cancelar',
        showLoaderOnConfirm: true, // Muestra un spinner mientras carga
        preConfirm: (codigoIngresado) => {
            // Hacemos la petición a tu nueva URL
            return fetch('/financings/validar-codigo-seguridad/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Si no usas @csrf_exempt, aquí deberías enviar el X-CSRFToken
                },
                body: JSON.stringify({ codigo: codigoIngresado })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la red');
                }
                return response.json();
            })
            .catch(error => {
                Swal.showValidationMessage(`Solicitud fallida: ${error}`);
            });
        },
        allowOutsideClick: () => !Swal.isLoading()
    }).then((result) => {
        if (result.isConfirmed) {
            // result.value contiene la respuesta de tu JsonResponse
            if (result.value.valido) {
                Swal.fire({
                    title: '¡Éxito!',
                    text: 'Código verificado correctamente.',
                    icon: 'success',
                    timer: 1500,
                    showConfirmButton: false
                });
                
                // Un pequeño delay para que el usuario vea el éxito antes de redirigir
                setTimeout(() => {
                    formElement.submit();
                }, 1000);
                
            } else {
                Swal.fire('Error', 'El código ingresado es incorrecto.', 'error');
            }
        }
    });
}