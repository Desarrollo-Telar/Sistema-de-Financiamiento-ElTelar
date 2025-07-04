import { Vehiculo } from '../../class/type_guarantee.js';

import { ocultar } from './ocultar_mostrar.js'
import { clearFields } from './limpiador.js'

// Evento para agregar una hipoteca
export function agregar_vehiculo(addGuarantee) {
    // Evento para agregar un Vehiculo
    document.getElementById('agregar_garantiaV').addEventListener('click', function (event) {
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
        //vehiculo.fotografias = document.getElementById('fotografiaC').files[0];
        //vehiculo.tarjetaCirculacion = document.getElementById('tarjetaC').files[0];
        //vehiculo.titulo = document.getElementById('tituloC').files[0];
        vehiculo.noPoliza = document.getElementById('noPoliza5').value;
        vehiculo.montoSeguro = document.getElementById('montoSeguroC').value;
        vehiculo.noContratoArrendamiento = document.getElementById('arrendamientoC').value;




        addGuarantee('VEHICULO', vehiculo.toJSON());
        clearFields();
        ocultar(document.getElementById('vehiculo'));
        document.getElementById('tipo_garantia').value = 0;


    });


}
