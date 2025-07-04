import { recoletarInformacionDirecciones } from '../../customer/recolectar.js';


export async function postDireccion(url, customer_id) {
    try {
        let direccionData = recoletarInformacionDirecciones(customer_id);
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
        alert('ERROR: ',error);
        console.error('Error en el envío de direcciones:', error);
        throw error;
    }
}




