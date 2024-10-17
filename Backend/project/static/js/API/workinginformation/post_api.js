

import { recolectarInformacionLaboral } from '../../customer/recolectar.js';


export async function postLaboral(customer_id) {
    try {
        let informacionLaboral = recolectarInformacionLaboral(customer_id);
        let sourceOfIncome1 = document.getElementById('source_of_income1').value;

        let url = sourceOfIncome1 === 'Otra'
            ? 'http://127.0.0.1:8000/financial_information/api/other_sources/'
            : 'http://127.0.0.1:8000/financial_information/api/working_information/';
        
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



