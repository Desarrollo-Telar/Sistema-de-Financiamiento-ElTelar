import { urls } from '../urls_api.js'

export const list_customer = fetch(urls.api_url_otra_informacion_laboral)
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));