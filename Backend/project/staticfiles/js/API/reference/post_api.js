import { recoletarInformacionReferencias } from '../../customer/recolectar.js';

export async function postReferencia(url, customer_id) {
    try {
        let direccionData = recoletarInformacionReferencias(customer_id);
        let direc = direccionData.map(direccion => direccion.toJSON());

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        for (const direccion of direc) {
            const response = await axios.post(url, direccion, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Incluir el token CSRF en las cabeceras
                }
            });

            console.log('Respuesta de la API:', response.data);
        }
    } catch (error) {
        alert('Error: ',error);
        console.error('Error en el envío de referencias:', error);
        throw error;
    }
}

