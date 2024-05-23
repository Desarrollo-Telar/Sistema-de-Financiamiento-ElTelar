
const mostrar = (elemento) => {
    elemento.style.display = 'block';
};

const ocultar = (elemento) => {
    elemento.style.display = 'none';
};

const mostrarOcultar = (id1, id2, id3 = null) => {
    console.log(id1, id2, id3);
    let div = document.getElementById(id1);
    let div2 = document.getElementById(id2);
    let div3 = id3 ? document.getElementById(id3) : null;

    if (window.getComputedStyle(div).display !== 'none') {
        ocultar(div);
        if (div3) {
            ocultar(div3);
        }
        mostrar(div2);
        return false;
    }
    mostrar(div);
    ocultar(div2);
    if (div3) {
        mostrar(div3);
    }
};
