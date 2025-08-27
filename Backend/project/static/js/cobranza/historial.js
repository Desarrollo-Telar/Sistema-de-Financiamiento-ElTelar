document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.ver-detalles').forEach(function (link) {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const id_historial = this.dataset.historial_id;
            console.log(id_historial);
            //if (!id_historial) return;

            // Llamar a la API
            fetch(`/customers/api/historial-cobranza/${id_historial}/`)
                .then(response => response.json())
                .then(data => {
                    // Llenar campos del modal
                    document.getElementById('modal-accion').textContent = data.accion;
                    document.getElementById('modal-usuario').textContent = data.usuario;
                    document.getElementById('modal-fecha').textContent = new Date(data.fecha_cambio).toLocaleString();
                    document.getElementById('modal-observaciones').textContent = data.observaciones_cambio || 'Sin observaciones';

                    // Procesar datos anteriores
                    const datosAnt = data.datos_anteriores || {};
                    const datosAnterioresContainer = document.getElementById('modal-datos-anteriores');
                    if (Object.keys(datosAnt).length === 0) {
                        datosAnterioresContainer.innerHTML = '<p class="text-muted mb-0">Sin datos anteriores</p>';
                    } else {
                        datosAnterioresContainer.innerHTML = Object.entries(datosAnt)
                            .map(([k, v]) => `<p class="mb-1"><strong>${k}:</strong> ${v}</p>`)
                            .join('');
                    }

                    // Procesar datos nuevos
                    const datosNv = data.datos_nuevos || {};
                    const datosNuevosContainer = document.getElementById('modal-datos-nuevos');
                    if (Object.keys(datosNv).length === 0) {
                        datosNuevosContainer.innerHTML = '<p class="text-muted mb-0">Sin datos nuevos</p>';
                    } else {
                        datosNuevosContainer.innerHTML = Object.entries(datosNv)
                            .map(([k, v]) => `<p class="mb-1"><strong>${k}:</strong> ${v}</p>`)
                            .join('');
                    }

                    // Mostrar el modal
                    const modal = new bootstrap.Modal(document.getElementById('modalDetalles'));
                    modal.show();
                })
                .catch(error => {
                    console.error('Error al obtener historial:', error);
                    alert('No se pudo cargar la información.');
                });
        });
    });
});
