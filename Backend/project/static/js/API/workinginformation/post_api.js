

import { recolectarInformacionLaboral } from '../../customer/recolectar.js';


export async function postLaboral(customer_id) {
    try {
        let informacionLaboral = recolectarInformacionLaboral(customer_id);
        let sourceOfIncome1 = document.getElementById('source_of_income1').value;
        
        let url;

        if (sourceOfIncome1 === 'Otra'){
            url = 'http://127.0.0.1:8000/financial_information/api/other_sources/';

        }else{
            url = 'http://127.0.0.1:8000/financial_information/api/working_information/';
        }
        console.log(url);

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


