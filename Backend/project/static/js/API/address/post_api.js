import { recoletarInformacionDirecciones } from '../../customer/recolectar.js';
import {Coordenada} from '../../class/coordinate.js'
import {urls} from '../urls_api.js'

export async function postDireccion(url, customer_id) {
    try {
        let direccionData = recoletarInformacionDirecciones(customer_id);
        let direc = direccionData.map(direccion => direccion.toJSON());

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        for (const direccion of direc) {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Incluir el token CSRF en las cabeceras
                },
                body: JSON.stringify(direccion)
            });

            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.status}`);
            }

            const data = await response.json();
            console.log('Respuesta de la API:', data);
            const coordenadas = await postCoordena(data.id);
            console.log('Coordenadas registradas con exito:',coordenadas);
        }
    } catch (error) {
        console.error('Error en el envío de direcciones:', error);
        throw error;
    }
}

function recolectarInformacionCoordenas(address_id){
    let coordenadas = [
        new Coordenada(),
        new Coordenada()
    ];

    coordenadas[0].latitud = document.getElementById('latitud1').value;
    coordenadas[0].longitud = document.getElementById('longitud1').value;
    coordenadas[0].address_id = address_id;

    coordenadas[1].latitud = document.getElementById('latitud2').value;
    coordenadas[1].longitud = document.getElementById('longitud2').value;
    coordenadas[1].address_id = address_id;

    return coordenadas;
}

async function postCoordena(address_id) {
    try {
        let coordenadaData = recolectarInformacionCoordenas(address_id);
        let coordenadas = coordenadaData.map(coordenada => coordenada.toJSON());

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const promises = coordenadas.map(async (coordenada) => {
            const response = await fetch(urls.api_url_direccion_coordenadas, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Incluir el token CSRF en las cabeceras
                },
                body: JSON.stringify(coordenada)
            });

            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.status}`);
            }

            return await response.json();
        });

        const results = await Promise.all(promises);
        results.forEach(result => console.log('Respuesta de la API:', result));
        return results;
    } catch (error) {
        console.error('Error en el envío de coordenadas:', error);
        throw error;
    }
}