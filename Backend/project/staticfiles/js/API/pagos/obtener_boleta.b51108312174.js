import {urls_p} from '../urls_api.js'


export async function get_boleta(boleta_numero_referencia) {
    try {
      const response = await axios.get(`${urls_p.api_url_pago}?term=${boleta_numero_referencia}`);
      console.log(response);
      return response.data;
    } catch (error) {
      console.error(error);
      return error;
    }
  }