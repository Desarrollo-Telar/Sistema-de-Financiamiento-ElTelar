
import { urls } from '../urls_api.js'

export const list_customer = fetch(urls.api_url_direccion)
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));