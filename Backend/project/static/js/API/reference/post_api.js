import { recoletarInformacionReferencias } from '../../customer/recolectar.js';

export async function postReferencia(url, customer_id) {
    try {
        let referenciaData = recoletarInformacionReferencias(customer_id);

        let refe = [
            referenciaData[0].toJSON(),
            referenciaData[1].toJSON(),
            referenciaData[2].toJSON(),
            referenciaData[3].toJSON(),
        ];

        // Obtener el token CSRF del meta tag una sola vez
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        // Usar un bucle for...of para iterar sobre cada referencia y enviar la solicitud
        for (const renfe of refe) {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Incluir el token CSRF en las cabeceras
                },
                body: JSON.stringify(renfe)
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }

            const data = await response.json();
            console.log(data);
            return data;
        }
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}
