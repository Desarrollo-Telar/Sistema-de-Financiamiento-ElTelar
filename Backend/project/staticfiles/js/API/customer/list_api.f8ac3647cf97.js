import { urls } from '../urls_api.js';

export async function fetchCustomerList() {
    return fetch(urls.api_url_cliente)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener la lista de clientes: ' + response.statusText);
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



export function filtros(atributo, valor) {
    list = [];
    fetchCustomerList()
        .then(customers => {
            // Hacer algo con la lista de clientes, como mostrarla en la interfaz de usuario
            console.log(customers)
            if (customers[`${atributo}`] === valor){
                list = customers;
            }
        })
        .catch(error => {
            // Manejar el error, por ejemplo, mostrando un mensaje de error al usuario
            console.error(error);
        });
    
    

    
}

export async function filtro(atributo, valor) {
    try {
        const customers = await fetchCustomerList();
        const filteredList = customers.filter(customer => customer[atributo] === valor);
        console.log(filteredList);
        return filteredList;
    } catch (error) {
        console.error('Error en el filtro:', error);
        throw error;
    }
}
