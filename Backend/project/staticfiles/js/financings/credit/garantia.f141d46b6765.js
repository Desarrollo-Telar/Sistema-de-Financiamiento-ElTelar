import { Guarantee, DetailGuarantee } from '../../class/guarantee.js';
import { Hipoteca, Cheque, DerechoDePosesionHipoteca, Fiador, Mobiliaria, Vehiculo} from '../../class/type_guarantee.js';

const tbody_garantia = document.getElementById('tbody_garantia');
const suma = document.getElementById('total_garantia');
export const lista_garantia = [];
import {urls, urls_p} from '../../API/urls_api.js'

export let suma_total = '';

// Función para actualizar la suma total
function garantias() {
    const garantia = new Guarantee(lista_garantia);
    suma.innerText = `Q ${garantia._suma_total}`;
    suma_total = garantia._suma_total;
}

// Función genérica para agregar una nueva garantía
function addGuarantee(tipoGarantia, especificacion) {
    const tipo = {
        garantia_id:1,
        tipo_garantia: tipoGarantia,
        valor_cobertura: parseFloat(document.getElementById('valor_cobertura').value),
        especificacion: especificacion
    };
    
    lista_garantia.push(tipo);
    
    // Añadir una nueva fila en la tabla
    var nueva_fila = tbody_garantia.insertRow();
    nueva_fila.insertCell(0).textContent = tipo['tipo_garantia'];
    nueva_fila.insertCell(1).textContent = JSON.stringify(tipo['especificacion'], null, 2); // Convertir a JSON legible
    nueva_fila.insertCell(2).textContent = `Q ${tipo['valor_cobertura']}`;
    
    var btn_remove = nueva_fila.insertCell(3);
    let btnDelete = document.createElement("button");
    btnDelete.textContent = "Eliminar";
    btnDelete.type = "button";
    btnDelete.style = "background-color:#52be80; color: #effaf3; border: 1px solid #52be80; border-radius: 2rem;";
    btn_remove.appendChild(btnDelete);

    // Añadir event listener al botón de eliminar
    btnDelete.addEventListener("click", function(event) {
        var fila = event.target.parentNode.parentNode;
        var index = Array.from(tbody_garantia.children).indexOf(fila);

        tbody_garantia.removeChild(fila);
        lista_garantia.splice(index, 1); // Eliminar de la lista de garantías

        garantias(); // Actualizar la suma total
    });
    
    garantias();
}

// Función para limpiar campos del formulario
function clearFields() {
    document.getElementById('noEscritura').value = '';
    document.getElementById('notario').value = '';
    document.getElementById('finca').value = '';
    document.getElementById('folio').value = '';
    document.getElementById('libro').value = '';
    document.getElementById('area').value = '';
    document.getElementById('ubicacion').value = '';
    document.getElementById('descripcion').value = '';
    document.getElementById('valor_comercial').value = '';
    document.getElementById('titular').value = '';
    document.getElementById('estatus').value = '';
    document.getElementById('noContratoArrendamiento').value = '';
    document.getElementById('avaluoBien').value = '';
    document.getElementById('docDigitalSoporte').value = '';
    document.getElementById('valor_cobertura').value = '';
    document.getElementById('noCheque').value = '';
    document.getElementById('nombreCuenta').value= '';
    document.getElementById('banco').value= '';
    document.getElementById('cheque_girado_a').value= '';
    document.getElementById('monto_cheque').value= '';
    document.getElementById('cheque').value= '';
}

// Evento para agregar una hipoteca
document.getElementById('agregar_garantiaH').addEventListener('click', function(event) {
    event.preventDefault();
    
    let valor_cobertura = document.getElementById('valor_cobertura').value;
    if (!valor_cobertura || valor_cobertura === '') {
        alert('DEBE DE INGRESAR EL VALOR DE COBERTURA');
        return; // Cambiado para evitar el uso de `throw` en un evento DOM
    }

    const hipoteca = new Hipoteca();
    hipoteca.noEscritura = document.getElementById('noEscritura').value;
    hipoteca.notario = document.getElementById('notario').value;
    hipoteca.finca = document.getElementById('finca').value;
    hipoteca.folio = document.getElementById('folio').value;
    hipoteca.libro = document.getElementById('libro').value;
    hipoteca.area = document.getElementById('area').value;
    hipoteca.ubicacion = document.getElementById('ubicacion').value;
    hipoteca.descripcion = document.getElementById('descripcion').value;
    hipoteca.valor_comercial = document.getElementById('valor_comercial').value;
    hipoteca.titular = document.getElementById('titular').value;
    hipoteca.estatus = document.getElementById('estatus').value;
    hipoteca.noContratoArrendamiento = document.getElementById('noContratoArrendamiento').value;
    hipoteca.avaluoBien = document.getElementById('avaluoBien').value;
    hipoteca.docDigitalSoporte = document.getElementById('docDigitalSoporte').value;

    addGuarantee('HIPOTECA', hipoteca.toJSON());
    clearFields();
});

// Evento para agregar un cheque
document.getElementById('agregar_garantiaC').addEventListener('click', function(event) {
    event.preventDefault();
    
    let valor_cobertura = document.getElementById('valor_cobertura').value;
    if (!valor_cobertura || valor_cobertura === '') {
        alert('DEBE DE INGRESAR EL VALOR DE COBERTURA');
        return; // Cambiado para evitar el uso de `throw` en un evento DOM
    }

    const cheque = new Cheque();
    cheque.noCheque = document.getElementById('noCheque').value;
    cheque.nombreCuenta = document.getElementById('nombreCuenta').value;
    cheque.banco = document.getElementById('banco').value;
    cheque.cheque_girado_a = document.getElementById('cheque_girado_a').value;
    cheque.monto_cheque = document.getElementById('monto_cheque').value;
    cheque.fotografia_cheque = document.getElementById('cheque').value;

    addGuarantee('CHEQUE', cheque.toJSON());
    clearFields();
});

// Evento para agregar un Derecho de posesion hipoteca
document.getElementById('agregar_garantiaDH').addEventListener('click',function(event){
    event.preventDefault();
    
    let valor_cobertura = document.getElementById('valor_cobertura').value;
    if (!valor_cobertura || valor_cobertura === '') {
        alert('DEBE DE INGRESAR EL VALOR DE COBERTURA');
        return; // Cambiado para evitar el uso de `throw` en un evento DOM
    }
    const dh = new DerechoDePosesionHipoteca();
    dh.noEscritura = document.getElementById('noEscritura1').value;
    dh.notario = document.getElementById('notario1').value;
    dh.area = document.getElementById('area1').value;
    dh.ubicacion = document.getElementById('ubicacion1').value;
    dh.descripcion = document.getElementById('descripcion1').value;
    dh.valor_comercial = document.getElementById('valor_comercial1').value;
    dh.titular = document.getElementById('titular1').value;
    dh.estatus = document.getElementById('estatus1').value;
    dh.noContratoArrendamiento = document.getElementById('noContratoArrendamiento1').value;
    dh.avaluoBien = document.getElementById('avaluoBien1').value;
    dh.docDigitalSoporte = document.getElementById('docDigitalSoporte1').value;

    addGuarantee('DERECHO DE POSESION HIPOTECA', dh.toJSON());
    clearFields();

});

// Evento para agregar un Fiador
document.getElementById('agregar_garantiaF').addEventListener('click', function(event){
    event.preventDefault();
    
    let valor_cobertura = document.getElementById('valor_cobertura').value;
    if (!valor_cobertura || valor_cobertura === '') {
        alert('DEBE DE INGRESAR EL VALOR DE COBERTURA');
        return; // Cambiado para evitar el uso de `throw` en un evento DOM
    }
    const fiador = new Fiador()
     
    fiador.codigo_cliente = document.getElementById('fiador_codigo_cliente').value;
    fiador.numeroTelefono = document.getElementById('telefono2').value;
    fiador.lugar_trabajo = document.getElementById('lugar_trabajo').value;
    fiador.ingresos = document.getElementById('ingreso').value;
    fiador.fotografia = document.getElementById('fotografiaF').value;


    addGuarantee('FIADOR', fiador.toJSON());
    clearFields();
});

// Evento para agregar un Mobiliaria
document.getElementById('agregar_garantiaM').addEventListener('click',function(event){
    event.preventDefault();
    
    let valor_cobertura = document.getElementById('valor_cobertura').value;
    if (!valor_cobertura || valor_cobertura === '') {
        alert('DEBE DE INGRESAR EL VALOR DE COBERTURA');
        return; // Cambiado para evitar el uso de `throw` en un evento DOM
    }
    const mobiliaria = new Mobiliaria();
    mobiliaria.descripcionBien = document.getElementById('descripcionBien').value;
    mobiliaria.documentoAcredita = document.getElementById('documentoAcredita1').value;
    mobiliaria.imagenDocumentoAcredita = document.getElementById('imagenDocumentoAcredita').value;
    mobiliaria.fotografiaBien = document.getElementById('fotografiaBien1').value;
    mobiliaria.noPoliza = document.getElementById('noPoliza1').value;
    mobiliaria.montoSeguro = document.getElementById('montoSeguro').value;
    



    addGuarantee('MOBILIARIA', mobiliaria.toJSON());
    clearFields();


});

// Evento para agregar un Vehiculo
document.getElementById('agregar_garantiaV').addEventListener('click',function(event){
    event.preventDefault();
    
    let valor_cobertura = document.getElementById('valor_cobertura').value;
    if (!valor_cobertura || valor_cobertura === '') {
        alert('DEBE DE INGRESAR EL VALOR DE COBERTURA');
        return; // Cambiado para evitar el uso de `throw` en un evento DOM
    }
    const vehiculo = new Vehiculo();
    vehiculo.placa = document.getElementById('placa').value;
    vehiculo.marca = document.getElementById('marca').value;
    vehiculo.color = document.getElementById('color').value;
    vehiculo.noChasis = document.getElementById('noChasis').value;
    vehiculo.noMotor = document.getElementById('noMotor').value;
    vehiculo.valor_comercial = document.getElementById('valor_comercial5').value;
    vehiculo.fotografias = document.getElementById('fotografiaC').value;
    vehiculo.tarjetaCirculacion = document.getElementById('tarjetaC').value;
    vehiculo.titulo = document.getElementById('tituloC').value;
    vehiculo.noPoliza = document.getElementById('noPoliza5').value;
    vehiculo.montoSeguro = document.getElementById('montoSeguroC').value;
    vehiculo.noContratoArrendamiento = document.getElementById('arrendamientoC').value;
    



    addGuarantee('VEHICULO', vehiculo.toJSON());
    clearFields();


});

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
