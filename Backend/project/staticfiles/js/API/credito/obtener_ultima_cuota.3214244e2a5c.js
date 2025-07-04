import {urls_p} from '../urls_api.js'

export async function get_ultima_cuota(credit_id_id) {
    try {
      const response = await axios.get(`${urls_p.api_url_cuota}?term=${credit_id_id}`);
      console.log(response);
      return response.data;
    } catch (error) {
      console.error(error);
      return error;
    }
  }