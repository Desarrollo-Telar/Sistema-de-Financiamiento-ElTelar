import {urls_p} from '../urls_api.js'

export function formato_fechas(fecha) {
    const date = new Date(fecha);
    const meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ];

    // Extraer día, mes y año
    const day = String(date.getDate()).padStart(2, '0'); // Asegura dos dígitos
    const month = meses[date.getUTCMonth()]; // Meses empiezan desde 0
    const year = date.getFullYear();
    return `${day} de ${month} de ${year}`;

}

export async function get_credit(credi_id) {
    try {
      const response = await axios.get(`${urls_p.api_url_credit}${credi_id}/`);
      console.log(response);
      return response.data;
    } catch (error) {
      console.error(error);
      return error;
    }
  }

export async function get_mensaje(credito, cuota) {
  const cliente = await get_credit(credito)
  
  return `Estimado ${cliente.customer_id.first_name} ${cliente.customer_id.last_name}.
Le recordamos la importancia de realizar su pago correspondiente, el total del monto a cancelar es de Q${cuota.total_cancelar} para su cuota No. ${cuota.mes}.
Tiene como fecha de pago el ${formato_fechas(cuota.due_date)}. Agradecemos su boleta de manera urgente para evitar recargos adicionales.`
}
  
