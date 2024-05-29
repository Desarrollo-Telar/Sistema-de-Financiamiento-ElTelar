

import { recoletarInformacionLaboral } from '../../customer/recolectar.js';
import { urls } from '../urls_api.js';

export async function postLaboral(customer_id) {
    try {
        let informacionLaboral = recoletarInformacionLaboral(customer_id);
        let sourceOfIncome1 = document.getElementById('source_of_income1').value;
        
        let url;

        if (sourceOfIncome1 === 'Otra'){
            url = urls.api_url_otra_informacion_laboral;

        }else{
            url = urls.api_url_informacion_laboral;
        }

        // Obtener el token CSRF del meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // Incluir el token CSRF en las cabeceras
            },
            body: JSON.stringify(informacionLaboral.toJSON())
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


