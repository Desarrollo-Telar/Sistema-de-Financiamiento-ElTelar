
import { recoletarInformacionDirecciones } from '../../customer/recolectar.js';

export async function putDireccion(url_api,id) {
    try {
        let direccionData = recoletarInformacionDirecciones();
        console.log(direccionData[0].toJSON());
        let url = `${url_api}${id}/`

        // Obtener el token CSRF del meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // Incluir el token CSRF en las cabeceras
            },
            body: JSON.stringify(direccionData[0].toJSON())
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}


