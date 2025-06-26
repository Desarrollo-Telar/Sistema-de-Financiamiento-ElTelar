import { Guarantee, DetailGuarantee } from '../../class/guarantee.js';



// FUNCIONES EXTERNAS
import {agregar_hipoteca} from '../funciones_externas/agregar_garantia_hipoteca.js';
import { agregar_cheque } from '../funciones_externas/agregar_garantia_cheque.js';
import { agregar_derecho_posesion } from '../funciones_externas/agregar_garantia_derecho_posesion.js';
import { agregar_fiador } from '../funciones_externas/agregar_garantia_fiador.js';
import { agregar_vehiculo } from '../funciones_externas/agregar_garantia_vehiculo.js';
import { agregar_mobiliaria } from '../funciones_externas/agregar_garantia_mobiliaria.js';

const tbody_garantia = document.getElementById('tbody_garantia');
const suma = document.getElementById('total_garantia');
export const lista_garantia = [];
export const list_form_data = [];
import {urls, urls_p} from '../../API/urls_api.js'

// ------ divs -----
export let suma_total = 0;

// Función para actualizar la suma total
function garantias() {
    const garantia = new Guarantee(lista_garantia);
    suma.innerText = `Q ${garantia._suma_total}`;
    suma_total = garantia._suma_total;
}

// Función genérica para agregar una nueva garantía
function addGuarantee(tipoGarantia, especificacion,formData=NaN) {
    console.log(especificacion)
    const tipo = {
        garantia_id:1,
        tipo_garantia: tipoGarantia,
        valor_cobertura: parseFloat(document.getElementById('valor_cobertura').value),
        especificacion: especificacion
    };
    
    const tipo_f = {
        garantia_id:1,
        tipo_garantia: tipoGarantia,
        valor_cobertura: parseFloat(document.getElementById('valor_cobertura').value),
        especificacion: formData
    };
    
    lista_garantia.push(tipo);
    list_form_data.push(tipo_f);
    
    // Añadir una nueva fila en la tabla
    var nueva_fila = tbody_garantia.insertRow();
    nueva_fila.insertCell(0).textContent = tipo['tipo_garantia'];
    nueva_fila.insertCell(1).textContent = JSON.stringify(tipo['especificacion'], null, 2); // Convertir a JSON legible
    nueva_fila.insertCell(2).textContent = `Q ${tipo['valor_cobertura']}`;
    
    var btn_remove = nueva_fila.insertCell(3);
    let btnDelete = document.createElement("button");
    btnDelete.textContent = "Eliminar";
    btnDelete.type = "button";
    btnDelete.classList.add('btn_cancel')
    btn_remove.appendChild(btnDelete);

    // Añadir event listener al botón de eliminar
    btnDelete.addEventListener("click", function(event) {
        var fila = event.target.parentNode.parentNode;
        var index = Array.from(tbody_garantia.children).indexOf(fila);

        tbody_garantia.removeChild(fila);
        lista_garantia.splice(index, 1); // Eliminar de la lista de garantías
        list_form_data.splice(index,1);

        garantias(); // Actualizar la suma total
    });
    
    garantias();
}



agregar_hipoteca(addGuarantee);
agregar_cheque(addGuarantee);
agregar_derecho_posesion(addGuarantee);
agregar_fiador(addGuarantee);
agregar_vehiculo(addGuarantee);
agregar_mobiliaria(addGuarantee);






if(document.getElementById('garantia')){
    document.getElementById('garantia').addEventListener('submit', async function (event) {
        event.preventDefault();
        try {
            const credi_id = document.getElementById('credit_id').value;
    
           
            const garantia = await registroGarantia(urls_p.api_url_garantia, credi_id);
            console.log(garantia);
            alert('¡Formulario enviado con éxito!');
            window.location.href = `/financings/credit/${credi_id}`;
    
    
        } catch (error) {
            console.error('Error al registrar los datos:', error);
            alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.');
        }
    });

}


async function registroGarantia(url, credito_id) {
    try {
        let json = {
            suma_total: suma_total,
            credit_id: credito_id,
            descripcion: 'REGISTRO DE GARANTIA',
        };

        console.log(json);

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const response = await axios.post(url, json, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        const data = response.data;
        console.log(data);
        const detalle = await registrarDetalle(urls_p.api_url_detalle_garantia, data.id);
        console.log(detalle);
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

async function registrarDetalle(url, garantia_id) {
    try {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        for (let element of lista_garantia) {
            let js = {
                garantia_id: garantia_id,
                tipo_garantia: element['tipo_garantia'],
                valor_cobertura: element['valor_cobertura'],
                especificaciones: element['especificacion'],
            };
            console.log(`DETALLE DE GARANTIA ${JSON.stringify(js)}`);

            const response = await axios.post(url, js, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });

            console.log('Respuesta de la API:', response.data);
        }
    } catch (error) {
        console.error('Error en el envío de detalles:', error);
        throw error;
    }
}
