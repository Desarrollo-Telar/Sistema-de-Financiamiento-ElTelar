// Obtener el protocolo (HTTP/HTTPS)
const protocolo = window.location.protocol; // Ejemplo: "https:"

// Obtener el dominio (hostname)
const dominio = window.location.hostname; // Ejemplo: "example.com"

// Obtener el puerto
const puerto = window.location.port; // Ejemplo: "8080" o "" si no está explícito
const baseUrl = `${protocolo}//${dominio}${puerto ? `:${puerto}` : ''}`;

const mostrarOcultar = (id1, id2 = null, id3 = null) => {
    // Obtener los elementos por sus IDs
    let div = document.getElementById(id1);
    let div2 = id2 ? document.getElementById(id2) : null;
    let div3 = id3 ? document.getElementById(id3) : null;


    // Asegurarse de que el elemento principal exista antes de continuar
    if (!div) {
        console.error(`El elemento con id ${id1} no existe.`);
        return;
    }

    // Verificar si el elemento principal está visible
    if (window.getComputedStyle(div).display !== 'none') {
        // Ocultar el elemento principal
        ocultar(div);

        // Ocultar el tercer elemento si existe
        if (div3) {
            ocultar(div3);
        }

        // Mostrar el segundo elemento si existe
        if (div2) {
            mostrar(div2);
        }

        return false;
    }

    // Mostrar el elemento principal
    mostrar(div);

    // Ocultar el segundo elemento si existe
    if (div2) {
        ocultar(div2);
    }

    // Mostrar el tercer elemento si existe
    if (div3) {
        mostrar(div3);
    }
};


// Definición de las funciones mostrar y ocultar
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


const mostrarFuente = (id) => {
    let div = document.getElementById(id);
    let informacionLaborl = document.getElementById('informacionLaboral');
    let direccion = document.getElementById('direccion');
    let otra = document.getElementById('otra');


    if (div.value === 'Otra') {

        mostrar(otra);
        mostrar(direccion);
        ocultar(informacionLaborl);
    } else {

        mostrar(informacionLaborl);
        mostrar(direccion);
        ocultar(otra);

    }
}

let id_type_of_transfers_or_transfer_of_funds = document.getElementById('transferencias');

ocultar(id_type_of_transfers_or_transfer_of_funds);

document.addEventListener('DOMContentLoaded', (event) => {
    // Obtener el checkbox por su ID
    const checkbox = document.getElementById('transfers_or_transfer_of_funds');
    // Obtener el párrafo para mostrar el estado
    //const status = document.getElementById('id_type_of_transfers_or_transfer_of_funds');

    // Añadir un listener para el evento 'change'
    checkbox.addEventListener('change', (event) => {
        if (checkbox.checked) {
            //status.textContent = 'Checkbox is checked';

            mostrar(id_type_of_transfers_or_transfer_of_funds);
        } else {
            //status.textContent = 'Checkbox is unchecked';

            ocultar(id_type_of_transfers_or_transfer_of_funds);
        }
    });
});

// ------------------- MANEJO PARA SUBIR IMAGEN ------------------------
const imagen_mostrar = document.getElementById('imagen_mostrar');
const pdf_mostrar = document.getElementById('pdf_mostrar');
// AQUI ESTAN LOS INPUTS PARA SUBIR LOS DOCUMENTOS
const pdf_dpi = document.getElementById('pdf_dpi');
const imagenes_dpi = document.getElementById('imagenes_dpi');

imagen_mostrar.addEventListener('input',function (event){
    let on = event.target.value;
    if(on){
        mostrar(imagenes_dpi);
        ocultar(pdf_dpi);
    }

});

pdf_mostrar.addEventListener('input',function (event){
    let on = event.target.value;
    if(on){
        ocultar(imagenes_dpi);
        mostrar(pdf_dpi);
    }

});


$(document).ready(function() {
    $('.asesor').select2({
        ajax: {
            url:  `${baseUrl}/customers/api/asesores/`,
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    term: params.term // Parámetro que el backend debe esperar
                };
            },
            processResults: function (data) {
                console.log(data);
                // Verificar si 'data' es un array de objetos
                if (Array.isArray(data)) {
                    return {
                        results: data.map(function (item) {
                            console.log(item);
                            return {
                                id: item.id,
                                text: item.nombre + ' '+item.apellido
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
        placeholder: 'Seleccione un Asesor',
        minimumInputLength: 1

    });
    
    $('.city1').select2({
        ajax: {
            url:  `${baseUrl}/addresses/api/departamento/`,
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    term: params.term // Parámetro que el backend debe esperar
                };
            },
            processResults: function (data) {
                console.log(data);
                // Verificar si 'data' es un array de objetos
                if (Array.isArray(data)) {
                    return {
                        results: data.map(function (item) {
                            console.log(item);
                            return {
                                id: item.id,
                                text: item.nombre
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
        placeholder: 'Seleccione un Departamento',
        minimumInputLength: 1

    });
    $(".state1").select2({
        ajax: {
            url:  `${baseUrl}/addresses/api/municipio/`,
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    term: params.term // Parámetro que el backend debe esperar
                };
            },
            processResults: function (data) {
                console.log(data);
                // Verificar si 'data' es un array de objetos
                if (Array.isArray(data)) {
                    return {
                        results: data.map(function (item) {
                            console.log(item);
                            return {
                                id: item.id,
                                text: item.nombre
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
        placeholder: 'Seleccione un Municipio',
        minimumInputLength: 1
    });
    $('.city2').select2({
        ajax: {
            url:  `${baseUrl}/addresses/api/departamento/`,
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    term: params.term // Parámetro que el backend debe esperar
                };
            },
            processResults: function (data) {
                console.log(data);
                // Verificar si 'data' es un array de objetos
                if (Array.isArray(data)) {
                    return {
                        results: data.map(function (item) {
                            console.log(item);
                            return {
                                id: item.id,
                                text: item.nombre
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
        placeholder: 'Seleccione un Departamento',
        minimumInputLength: 1

    });
    $(".state2").select2({
        ajax: {
            url:  `${baseUrl}/addresses/api/municipio/`,
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    term: params.term // Parámetro que el backend debe esperar
                };
            },
            processResults: function (data) {
                console.log(data);
                // Verificar si 'data' es un array de objetos
                if (Array.isArray(data)) {
                    return {
                        results: data.map(function (item) {
                            console.log(item);
                            return {
                                id: item.id,
                                text: item.nombre
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
        placeholder: 'Seleccione un Municipio',
        minimumInputLength: 1
    });
    
   
    
    
});