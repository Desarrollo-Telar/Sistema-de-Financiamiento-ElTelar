import { Guarantee, DetailGuarantee } from '../../class/guarantee.js';
import { Hipoteca, DerechoDePosesionHipoteca, Fiador, Cheque, Vehiculo, Mobiliaria } from '../../class/type_guarantee.js';

const tbody_garantia = document.getElementById('tbody_garantia');
const suma = document.getElementById('total_garantia');
const lista_garantia = [];

function garantias() {
    const garantia = new Guarantee(lista_garantia);
    suma.innerText = `Q ${garantia._suma_total}`;
}

// INFORMACIÓN DE TIPO DE GARANTÍA
const btn_addHipoteca = document.getElementById('agregar_garantiaH');
btn_addHipoteca.addEventListener('click', function(event) {
    event.preventDefault();
    
    let noEscritura = document.getElementById('noEscritura').value;
    let notario = document.getElementById('notario').value;
    let finca = document.getElementById('finca').value;
    let folio = document.getElementById('folio').value;
    let libro = document.getElementById('libro').value;
    let area = document.getElementById('area').value;
    let ubicacion = document.getElementById('ubicacion').value;
    let descripcion = document.getElementById('descripcion').value;
    let valor_comercial = document.getElementById('valor_comercial').value;
    let titular = document.getElementById('titular').value;
    let estatus = document.getElementById('tipo_garantia').value;
    let noContratoArrendamiento = document.getElementById('noContratoArrendamiento').value;
    let avaluoBien = document.getElementById('avaluoBien').value;
    let docDigitalSoporte = document.getElementById('docDigitalSoporte').value;
    let valor_cobertura = document.getElementById('valor_cobertura').value;
    
    const hipoteca = new Hipoteca();

    if (!valor_cobertura || valor_cobertura === '') {
        alert('DEBE DE INGRESAR EL VALOR DE COBERTURA');
        return; // Cambiado para evitar el uso de `throw` en un evento DOM
    }
 /*  
    hipoteca.noEscritura = noEscritura;
    hipoteca.notario = notario;
    hipoteca.finca = finca;
    hipoteca.folio = folio;
    hipoteca.libro = libro;
    hipoteca.area = area;
    hipoteca.ubicacion = ubicacion;
    hipoteca.descripcion = descripcion;
    hipoteca.valor_comercial = valor_comercial;
    hipoteca.titular = titular;
    hipoteca.estatus = estatus;
    hipoteca.noContratoArrendamiento = noContratoArrendamiento;
    hipoteca.avaluoBien = avaluoBien;
    hipoteca.docDigitalSoporte = docDigitalSoporte;
*/
    const tipo = {
        tipo_garantia: 'HIPOTECA',
        valor_cobertura: parseFloat(valor_cobertura),
        especificacion: hipoteca.toJSON()
    };
    
    lista_garantia.push(tipo);
    
    // Añadir una nueva fila en la tabla
    var nueva_fila = tbody_garantia.insertRow();
    var tipos = nueva_fila.insertCell(0);
    tipos.textContent = tipo['tipo_garantia'];
    
    var especificacion = nueva_fila.insertCell(1);
    especificacion.textContent = JSON.stringify(tipo['especificacion'], null, 2); // Convertir a JSON legible
    
    var valor = nueva_fila.insertCell(2);
    valor.textContent = `Q ${tipo['valor_cobertura']}`;
    
    var btn_remove = nueva_fila.insertCell(3);
    let btnDelete = document.createElement("button");
    btnDelete.textContent = "Eliminar";
    btnDelete.type = "button";
    btnDelete.style = "background-color:#52be80; color: #effaf3; border: 1px solid #52be80; border-radius: 2rem;";
    btn_remove.appendChild(btnDelete);

    btnDelete.addEventListener("click", function(event) {
        var fila = event.target.parentNode.parentNode;
        var tabla = fila.parentNode;
        var index = Array.from(tabla.children).indexOf(fila);

        tabla.removeChild(fila);
        lista_garantia.splice(index, 1); // Eliminar de la lista de garantías

        garantias(); // Actualizar la suma total
    });
    
    garantias();
    
    document.getElementById('valor_cobertura').value = null;
});
