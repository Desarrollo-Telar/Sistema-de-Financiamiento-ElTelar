export const ocultar = (element) => {
    if (element) {
        element.style.display = 'none';
    }
};

export const mostrar = (element) => {
    if (element) {
        element.style.display = 'block';
    }
};
document.addEventListener("DOMContentLoaded", function () {
    let valor_referencia = document.getElementById('id_numero_referencia').value;
    
    if (valor_referencia != '3696008759'){
        document.getElementById("chequeo_boleta_banrural").checked;
        document.querySelector('label[for="id_numero_referencia"]').style.display = '';
        mostrar(document.getElementById('id_numero_referencia'));

    }else{
        document.querySelector('label[for="id_numero_referencia"]').style.display = 'none';
        ocultar(document.getElementById('id_numero_referencia'));
        document.getElementById('id_numero_referencia').value = '';
    }
    



});

document.getElementById("chequeo_boleta_banrural").addEventListener("change", function() {
    if (this.checked) {
        document.querySelector('label[for="id_numero_referencia"]').style.display = '';
        mostrar(document.getElementById('id_numero_referencia'));
        document.getElementById('id_numero_referencia').value = '';
    } else {
        document.querySelector('label[for="id_numero_referencia"]').style.display = 'none';
        ocultar(document.getElementById('id_numero_referencia'));
    }
});
