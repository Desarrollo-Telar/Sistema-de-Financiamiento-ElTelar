import { urls_p } from "../../API/urls_api.js"
import {alerta_m} from '../../alertas/alertas.js'

export function generarLinkPago(customerCode, cuotaId) {
    const url = `${urls_p.api_url_mensaje_alerta_pago}${customerCode}/${cuotaId}/`;

    axios.get(url)
        .then(response => {
            const linkWhatsapp = response.data.whatsapp_link;
            console.log('Link generado:', linkWhatsapp);

            // Abrir el enlace en una nueva pestaña
            window.open(linkWhatsapp, '_blank');
        })
        .catch(error => {
            console.error('Error al generar link:', error);
            alerta_m('No se pudo generar el mensaje. Verifica el código del cliente o la cuota.', false)
            
        });
}