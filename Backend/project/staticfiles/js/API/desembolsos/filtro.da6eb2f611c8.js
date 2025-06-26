import { urls_p } from '../urls_api.js'


export async function get_desembolsos(codigo_credito) {
    try {
        const response = await axios.get(`${urls_p.api_url_desembolso}?term=${codigo_credito}`);
        console.log(response);
        return response.data;
    } catch (error) {
        console.error(error);
        return error;
    }
}