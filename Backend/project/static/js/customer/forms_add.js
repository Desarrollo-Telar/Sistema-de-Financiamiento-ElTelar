
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


const mostrarFuente = (id) =>{
    let div = document.getElementById(id);
    let informacionLaborl = document.getElementById('informacionLaboral');
    let direccion = document.getElementById('direccion');
    let otra = document.getElementById('otra');
    
    
    if(div.value === 'Otra'){
        console.log('Mostrar informacion laboral de otra');
        mostrar(otra);
        mostrar(direccion);
        ocultar(informacionLaborl);
    }else{
        console.log('Mostrar informacion laboral de otra');
        mostrar(informacionLaborl);
        mostrar(direccion);
        ocultar(otra);

    }
}

let id_type_of_transfers_or_transfer_of_funds = document.getElementById('transferencias');
console.log(id_type_of_transfers_or_transfer_of_funds);
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
            console.log('Checkbox is checked');
            mostrar(id_type_of_transfers_or_transfer_of_funds)
        } else {
            //status.textContent = 'Checkbox is unchecked';
            console.log('Checkbox is unchecked');
            ocultar(id_type_of_transfers_or_transfer_of_funds);
        }
    });
});
