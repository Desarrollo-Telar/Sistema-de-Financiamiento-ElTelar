import { Hipoteca } from '../../class/type_guarantee.js';

import {ocultar} from './ocultar_mostrar.js'
import {clearFields} from './limpiador.js'

// Evento para agregar una hipoteca
export function agregar_hipoteca(addGuarantee){
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
        hipoteca.avaluoBien = document.getElementById('avaluoBien').files[0];
        hipoteca.docDigitalSoporte = document.getElementById('docDigitalSoporte').files[0];
        
        addGuarantee('HIPOTECA', hipoteca.toJSON());
        clearFields();
        ocultar(document.getElementById('hipoteca'));
        document.getElementById('tipo_garantia').value = 0;
    });

}
