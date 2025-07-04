

import { recoletarInformacionCliente } from '../../customer/recolectar.js';

export async function postCustomer(url) {
    try {
        let clienteData = recoletarInformacionCliente();

        // Obtener el token CSRF del meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const response = await axios.post(url, clienteData.toJSON(), {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // Incluir el token CSRF en las cabeceras
            }
        });

        console.log(response.data);
        return response.data;
    } catch (error) {
        alert('ERROR: ',error);
        console.error('Error:', error);
        throw error;
    }
}



