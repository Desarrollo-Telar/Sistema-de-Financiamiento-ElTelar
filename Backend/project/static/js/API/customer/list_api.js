import { urls } from '../urls_api.js';

export function fetchCustomerList() {
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

fetchCustomerList()
    .then(customers => {
        // Hacer algo con la lista de clientes, como mostrarla en la interfaz de usuario
        console.log(customers)
    })
    .catch(error => {
        // Manejar el error, por ejemplo, mostrando un mensaje de error al usuario
    });

const inputField = document.getElementById('myInput');
const outputDiv = document.getElementById('output');
// Agregar un event listener para el evento input
inputField.addEventListener('input', function(event) {
    const inputValue = event.target.value;
    outputDiv.textContent = `Texto ingresado: ${inputValue}`;
});