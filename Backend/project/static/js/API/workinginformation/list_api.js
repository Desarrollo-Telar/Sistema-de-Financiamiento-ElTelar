import { urls } from '../urls_api.js'


async function fetchInformacion_laboral() {
    return fetch(urls.api_url_informacion_laboral)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al momento de obtener informacion laboral ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Lista de clientes obtenida:', data);
            return data; // Puedes devolver los datos si necesitas hacer algo con ellos
        })
        .catch(error => {
            console.error('Error al obtener la lista de clientes:', error);
            throw error; // Puedes relanzar el error para manejarlo en otra parte de tu aplicación si es necesario
        });

}
async function fetchOtraInformacion_laboral() {
    return fetch(urls.api_url_otra_informacion_laboral)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al momento de obtener informacion laboral ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Lista de clientes obtenida:', data);
            return data; // Puedes devolver los datos si necesitas hacer algo con ellos
        })
        .catch(error => {
            console.error('Error al obtener la lista de clientes:', error);
            throw error; // Puedes relanzar el error para manejarlo en otra parte de tu aplicación si es necesario
        });

}

export async function filtro(valor) {
    try {
        const laboral = await fetchInformacion_laboral();
        const otra = await fetchOtraInformacion_laboral();
        
        let filterList = [];
        
        if (laboral && laboral.length > 0) {
            filterList = laboral.filter(item => item['customer_id'] === valor);
        }
        
        if (filterList.length === 0 && otra && otra.length > 0) {
            filterList = otra.filter(item => item['customer_id'] === valor);
        }

        console.log(filterList);
        return filterList;

    } catch (error) {
        console.error('Error en el filtro', error);
        throw error;
    }
}
