

import { recoletarInformacionPlanInversion } from '../../customer/recolectar.js';

export async function postPlanInversion(url, customer_id) {
    try {
        let plan_inversion = recoletarInformacionPlanInversion(customer_id);
        console.log(plan_inversion.toJSON());

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const response = await axios.post(url, plan_inversion.toJSON(), {
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



