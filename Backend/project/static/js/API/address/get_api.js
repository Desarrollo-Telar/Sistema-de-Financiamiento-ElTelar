import {urls_p} from '../urls_api.js'

export async function get_municipio(id){
    try{
        const url = `${urls_p.api_url_municipio}${id}/`;
        const response = await axios.get(url);
        if (response.data) {
            console.log(response.data);
            return response.data['nombre'];
            

        } else {
            console.log('No se encontraron datos para el término de búsqueda:');
        }

    }catch (error) {
        console.error('Error al buscar el Municipio:', error.response || error.message);
        return error;
    }


}

export async function get_departamento(id){
    try{
        const url = `${urls_p.api_url_departamento}${id}/`;
        const response = await axios.get(url);
        if (response.data) {
            console.log(response.data)
            return response.data['nombre'];

        } else {
            console.log('No se encontraron datos para el término de búsqueda:');
        }

    }catch (error) {
        console.error('Error al buscar el Municipio:', error.response || error.message);
        return error;
    }


}