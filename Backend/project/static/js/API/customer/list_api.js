
import { urls } from '../urls_api.js'

export const list_customer = fetch(urls.api_url_cliente)
.then(response => {
    if (!response.ok) {
        throw new Error('La respuesta de la red no fue correcta ' + response.statusText);
    }
    return response.json()
})
.then(data => console.log(data))
.catch(error => console.error('Error:', error));