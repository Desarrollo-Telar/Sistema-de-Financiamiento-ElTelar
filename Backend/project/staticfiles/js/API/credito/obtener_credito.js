import {urls_p} from '../urls_api.js'


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