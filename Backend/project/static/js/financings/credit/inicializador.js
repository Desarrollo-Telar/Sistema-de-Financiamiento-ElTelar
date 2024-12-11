
import {urls_p} from '../../API/urls_api.js'

const plazo = document.getElementById('plazo');
const fecha_inicio = document.getElementById('fecha_inicio');
const fecha_vencimiento = document.getElementById('fecha_vencimiento');

fecha_inicio.addEventListener('input', function (event) {
    const plazoValue = parseInt(plazo.value, 10); // Obtén el valor del plazo
    const fechaInicioValue = new Date(event.target.value);
    if (!isNaN(plazoValue) && fechaInicioValue instanceof Date && !isNaN(fechaInicioValue)) {
        fechaInicioValue.setMonth(fechaInicioValue.getMonth() + plazoValue);
        fecha_vencimiento.value = fechaInicioValue.toISOString().split('T')[0];
    }
});

plazo.addEventListener('input', function (event) {
    const plazoValue = parseInt(event.target.value, 10); // Obtén el valor del plazo
    const fechaInicioValue = new Date(fecha_inicio.value);
    if (!isNaN(plazoValue) && fechaInicioValue instanceof Date && !isNaN(fechaInicioValue)) {
        fechaInicioValue.setMonth(fechaInicioValue.getMonth() + plazoValue);
        fecha_vencimiento.value = fechaInicioValue.toISOString().split('T')[0];
        console.log(fechaInicioValue.toISOString().split('T')[0]);
    }
});



$(document).ready(function () {
    $(".customer_id").select2({
        width: 'resolve',
        ajax: {
            url: urls_p.api_url_clientes_aceptados,
            dataType: 'json',
            delay: 250,
            processResults: function (data) {
                console.log(data);
                // Verificar si 'data' es un array de objetos
                if (Array.isArray(data)) {
                    return {
                        results: data.map(function (item) {
                            return {
                                id: item.id,
                                text: item.customer_code + ' ' + item.first_name + ' ' + item.last_name
                            };
                        })
                    };
                } else {
                    console.error('Estructura de datos inesperada:', data);
                    return {
                        results: []
                    };
                }
            },
            cache: true
        },
        placeholder: 'Seleccione un Cliente',
        minimumInputLength: 1
    });
    $(".customer_id_fiador").select2({
        width: 'resolve',
        ajax: {
            url:  urls_p.api_url_cliente,

            dataType: 'json',
            delay: 250,
            processResults: function (data) {
                console.log(data);
                // Verificar si 'data' es un array de objetos
                if (Array.isArray(data)) {
                    return {
                        results: data.map(function (item) {
                            return {
                                id: item.id,
                                text: item.customer_code + ' ' + item.first_name + ' ' + item.last_name
                            };
                        })
                    };
                } else {
                    console.error('Estructura de datos inesperada:', data);
                    return {
                        results: []
                    };
                }
            },
            cache: true
        },
        placeholder: 'Seleccione un Cliente',
        minimumInputLength: 1
    });
    async function fetchInformacion_laboral() {

        return fetch(urls_p.api_url_informacion_laboral)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al momento de obtener informacion laboral ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log('Lista de clientes de informacion laboral obtenida:', data);
                return data; // Puedes devolver los datos si necesitas hacer algo con ellos
            })
            .catch(error => {
                console.error('Error al obtener la lista de clientes:', error);
                throw error; // Puedes relanzar el error para manejarlo en otra parte de tu aplicación si es necesario
            });

    }
    async function fetchOtraInformacion_laboral() {

        return fetch(urls_p.api_url_otra_informacion_laboral)
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

    async function filtro(valor) {
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


    $(".customer_id_fiador").on('select2:select', async function (e) {
        var data = e.params.data;
        var clienteId = data.id;
        var codigo_cliente = document.getElementById('fiador_codigo_cliente');
        var telefono = document.getElementById('telefono2');
        var lugar_trabajo = document.getElementById('lugar_trabajo');
        var ingreso = document.getElementById('ingreso');

        try {
            const laboral = await filtro(clienteId);
            laboral.forEach(element => {
                if (element.company_name) {
                    lugar_trabajo.value = element.company_name;

                } else {
                    lugar_trabajo.value = element.source_of_income;
                }

                ingreso.value = element.salary;
                console.log(element);
            });

            // Realizar una solicitud para obtener detalles adicionales del cliente
            const response = await fetch(`${urls_p.api_url_cliente}${clienteId}/`);
            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.statusText}`);
            }
            const clienteDetalles = await response.json();
            codigo_cliente.value = clienteDetalles.customer_code;
            telefono.value = clienteDetalles.telephone;
            // Aquí puedes usar los detalles de cliente para llenar otros campos, como lugar_trabajo e ingreso
        } catch (error) {
            console.error('Error obteniendo detalles del cliente:', error);
        }
    });

});
const tipo_garantia = document.getElementById('tipo_garantia');

const hipoteca = document.getElementById('hipoteca');
const derecho_posesion = document.getElementById('derecho_posesion');
const cheque = document.getElementById('cheque');
const fiador = document.getElementById('fiador');
const mobiliaria = document.getElementById('mobiliaria');
const vehiculo = document.getElementById('vehiculo');

tipo_garantia.addEventListener('change', function (event) {
    const valor = event.target.value;
    if (valor === 'HIPOTECA') {
        mostrar(hipoteca);
        ocultar(derecho_posesion);
        ocultar(cheque);
        ocultar(fiador);
        ocultar(mobiliaria);
        ocultar(vehiculo);

    } else if (valor === 'DERECHO DE POSESIÓN HIPOTECA') {
        ocultar(hipoteca);
        ocultar(cheque);
        mostrar(derecho_posesion);
        ocultar(fiador);
        ocultar(mobiliaria);
        ocultar(vehiculo);


    } else if (valor === 'FIADOR') {
        ocultar(hipoteca);
        ocultar(derecho_posesion);
        ocultar(cheque);
        mostrar(fiador);
        ocultar(mobiliaria);
        ocultar(vehiculo);

    } else if (valor === 'CHEQUE') {
        ocultar(hipoteca);
        ocultar(derecho_posesion);
        mostrar(cheque);
        ocultar(fiador);
        ocultar(mobiliaria);
        ocultar(vehiculo);

    } else if (valor === 'VEHICULO') {
        ocultar(hipoteca);
        ocultar(derecho_posesion);
        ocultar(fiador);
        ocultar(mobiliaria);
        mostrar(vehiculo);

    } else if (valor === 'MOBILIARIA') {
        ocultar(hipoteca);
        ocultar(derecho_posesion);
        ocultar(fiador);
        mostrar(mobiliaria);
        ocultar(vehiculo);

    } else {
        ocultar(hipoteca);
        ocultar(derecho_posesion);
        ocultar(cheque);
        ocultar(fiador);
        ocultar(mobiliaria);
        ocultar(vehiculo);
        console.log('Buenoooo');
    }
});

const ocultar = (element) => {
    if (element) {
        element.style.display = 'none';
    }
};

const mostrar = (element) => {
    if (element) {
        element.style.display = 'block';
    }
};



