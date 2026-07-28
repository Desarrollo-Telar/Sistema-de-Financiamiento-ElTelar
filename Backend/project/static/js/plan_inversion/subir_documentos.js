import { urls_p } from '../API/urls_api.js';

const uploadBtn = document.getElementById('uploadBtn');

uploadBtn.addEventListener('click', async () => {
    if (uploadedFiles.length === 0) {
       
        Swal.fire({
            icon: "error",
            title: "Error",
            text: 'Selecciona al menos un archivo para subir.',
            timer: 7000,
            showConfirmButton: false,
        });
        return;
    }

    // Asegúrate de tener el ID del expediente disponible
    const expedienteId = document.getElementById('expedienteId').value;
    const codigo = document.getElementById('codigo').value;

    // Obtener el Token CSRF de las cookies de Django
    const csrfToken = getCookie('csrftoken');

    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Subiendo...';

    try {
        // Subimos cada archivo de la lista
        const uploadPromises = uploadedFiles.map(async (item) => {
            const formData = new FormData();
            
            // "archivo" y "expediente" deben coincidir con los campos de tu modelo/serializer
            formData.append('archivo', item.file);
            formData.append('nombre_archivo', item.file.name);
            formData.append('expediente', expedienteId);

            const response = await fetch(urls_p.api_url_documento_expediente, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                    // NOTA: No agregues 'Content-Type', fetch lo configura automáticamente con FormData
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Error al subir ${item.file.name}`);
            }

            return response.json();
        });

        await Promise.all(uploadPromises);

        Swal.fire({
            icon: "success",
            title: "Registro Completado",
         
            timer: 500,
            showConfirmButton: false,
        });

        
        // Limpiamos la lista local tras subir
        uploadedFiles.forEach(f => URL.revokeObjectURL(f.url));
        uploadedFiles = [];
        renderFileList();

        setTimeout(() => { window.location.href = `/plan_inversion/lista_expedientes_notarios/${codigo}/`; }, 1000);

    } catch (error) {
        console.error(error);
        
        Swal.fire({
            icon: "error",
            title: "Error",
            text: 'Ocurrió un error al subir los archivos.',
            timer: 7000,
            showConfirmButton: false,
        });
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Subir Archivos';
    }
});

// Función auxiliar para leer la cookie CSRF que envía @ensure_csrf_cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}