

import { recolectarInformacionLaboral } from '../../customer/recolectar.js';
import {urls_p, urls} from '../urls_api.js'

export async function postLaboral(customer_id) {
    try {
        let informacionLaboral = recolectarInformacionLaboral(customer_id);
        let sourceOfIncome1 = document.getElementById('source_of_income1').value;

        let url = sourceOfIncome1 === 'Otra'
            ? urls_p.api_url_otra_informacion_laboral
            :urls_p.api_url_informacion_laboral;
        
        console.log(url);

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const response = await axios.post(url, informacionLaboral.toJSON(), {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        console.log(response.data);
        return response.data;
    } catch (error) {
        alert('Error: ',error);
        console.error('Error:', error);
        throw error;
    }
}



