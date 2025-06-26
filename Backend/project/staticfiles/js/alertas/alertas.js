export function alerta_m(mensaje, estado=false){
    if (!estado) {
        Swal.fire({
            icon: "error",
            title: `${mensaje}`,
            timer: 3000,
            showConfirmButton: false,
        });

    } else {
        Swal.fire({
            icon: "success",
            title: `${mensaje}`,
            timer: 3000,
            showConfirmButton: false,
        });

    }

}