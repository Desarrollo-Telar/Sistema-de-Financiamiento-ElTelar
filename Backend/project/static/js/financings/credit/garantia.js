import { Guarantee, DetailGuarantee } from '../../class/guarantee.js';
import { Hipoteca, Cheque } from '../../class/type_guarantee.js';

const tbody_garantia = document.getElementById('tbody_garantia');
const suma = document.getElementById('total_garantia');
const lista_garantia = [];

// Función para actualizar la suma total
function garantias() {
    const garantia = new Guarantee(lista_garantia);
    suma.innerText = `Q ${garantia._suma_total}`;
}

// Función genérica para agregar una nueva garantía
function addGuarantee(tipoGarantia, especificacion) {
    const tipo = {
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
    document.getElementById('tipo_garantia').value = '';
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
    hipoteca.estatus = document.getElementById('tipo_garantia').value;
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
