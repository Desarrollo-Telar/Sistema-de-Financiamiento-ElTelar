// Obtener el protocolo (HTTP/HTTPS)
const protocolo = window.location.protocol; // Ejemplo: "https:"

// Obtener el dominio (hostname)
const dominio = window.location.hostname; // Ejemplo: "example.com"

// Obtener el puerto
const puerto = window.location.port; // Ejemplo: "8080" o "" si no está explícito
const baseUrl = `${protocolo}//${dominio}${puerto ? `:${puerto}` : ''}`;

export const urls = {
    api_url_cliente : 'http://127.0.0.1:8000/customers/api/customers/',
    api_url_condicion_migratoria : 'http://127.0.0.1:8000/customers/api/immigration_status/',
    api_url_direccion: 'http://127.0.0.1:8000/addresses/api/address/',
    api_url_referencia: 'http://127.0.0.1:8000/financial_information/api/reference/',
    api_url_informacion_laboral:'http://127.0.0.1:8000/financial_information/api/working_information/',
    api_url_otra_informacion_laboral:'http://127.0.0.1:8000/financial_information/api/other_sources/',
    api_url_usuarios:'http://127.0.0.1:8000/users/api/users/',
    api_url_rol:'http://127.0.0.1:8000/roles&permissions/api/role/',
    api_url_investment_plan:'http://127.0.0.1:8000/plan_inversion/api/plan_inversion/',
    api_url_imagen:'http://127.0.0.1:8000/imagen/api/imagen/',
    api_url_imagen_cliente:'http://127.0.0.1:8000/imagen/api/imagen_cliente/',
    api_url_imagen_direccion:'http://127.0.0.1:8000/imagen/api/imagen_direccion/',
    api_url_desembolso:'http://127.0.0.1:8000/financings/api/desembolso/'
    
}

export const urls_p = {
    // CLIENTE
    api_url_cliente: `${baseUrl}/customers/api/customers/`,
    api_url_clientes_aceptados: `${baseUrl}/customers/api/customers_accept/`,
    api_url_condicion_migratoria:  `${baseUrl}/customers/api/immigration_status/`,

    // DIRECCION
    api_url_direccion:  `${baseUrl}/addresses/api/address/`,
    api_url_departamento:  `${baseUrl}/addresses/api/departamento/`,
    api_url_municipio:  `${baseUrl}/addresses/api/municipio/`,

    // INFORMACION FINANCIERA
    api_url_referencia:  `${baseUrl}/financial_information/api/reference/`,
    api_url_informacion_laboral: `${baseUrl}/financial_information/api/working_information/`,
    api_url_otra_informacion_laboral: `${baseUrl}/financial_information/api/other_sources/`,

    // USUARIOS
    api_url_usuarios: `${baseUrl}/users/api/users/`,

    // ROL
    api_url_rol: `${baseUrl}/roles&permissions/api/role/`,

    // PLAN DE INVERSION (DESTINO)
    api_url_investment_plan: `${baseUrl}/plan_inversion/api/plan_inversion/`,

    // IMAGENES
    api_url_imagen: `${baseUrl}/imagen/api/imagen/`,
    api_url_imagen_cliente: `${baseUrl}/imagen/api/imagen_cliente/`,
    api_url_imagen_direccion: `${baseUrl}/imagen/api/imagen_direccion/`,

    // FINANZAS
    api_url_credit: `${baseUrl}/financings/api/credit/`,
    api_url_credit_vigente: `${baseUrl}/financings/api/credit-vigente/`,
    api_url_garantia: `${baseUrl}/financings/api/garantia/`,
    api_url_detalle_garantia: `${baseUrl}/financings/api/detalle_garantia/`,
    api_url_desembolso: `${baseUrl}/financings/api/desembolso/`,
    api_url_pago: `${baseUrl}/financings/api/payment/`,
    api_url_cuota: `${baseUrl}/financings/api/cuota/`,
    api_url_cuotas: `${baseUrl}/financings/api/cuotas/`,
    api_url_estado_cuenta: `${baseUrl}/financings/api/estado_cuenta/`,

    // DOCUMENTOS
    api_url_documento_garantia: `${baseUrl}/documents/api/documento_garantia/`,

}