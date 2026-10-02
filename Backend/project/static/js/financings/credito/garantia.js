import { showToast } from './style.js';
let guaranteeList = [];


function renderDynamicGuaranteeFields() {

    const tipo = event.target.value;
    alert(`Tipo de garantía seleccionado: ${tipo}`); // Muestra el tipo de garantía seleccionado
    const container = document.getElementById('dynamic-guarantee-fields');
    container.innerHTML = '';

    let fieldsHTML = '';

    if (tipo === 'DERECHO DE POSESION HIPOTECA') {
        fieldsHTML = `
            <div><label class="block text-xs text-brandGrayText mb-1">Nombre</label><input type="text" id="json_nombre" class="glass-input w-full p-2 rounded-xl text-sm" value="DERECHO DE POSESIÓN HIPOTECA"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">No. Escritura</label><input type="text" id="json_no_escritura" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Notario</label><input type="text" id="json_notario" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Área (m²)</label><input type="text" id="json_area" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div class="md:col-span-2"><label class="block text-xs text-brandGrayText mb-1">Ubicación</label><input type="text" id="json_ubicacion" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div class="md:col-span-2"><label class="block text-xs text-brandGrayText mb-1">Descripción</label><input type="text" id="json_descripcion" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Valor Comercial (Q)</label><input type="number" id="json_valor_comercial" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Titular</label><input type="text" id="json_titular" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Estatus</label><input type="text" id="json_estatus" class="glass-input w-full p-2 rounded-xl text-sm" value="GRAVAMEN HIPOTECARIO"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">No. Contrato Arrendamiento</label><input type="text" id="json_no_contrato" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Avalúo Bien</label><input type="text" id="json_avaluo" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            
        `;
    } else if (tipo === 'HIPOTECA') {
        fieldsHTML = `
            <div><label class="block text-xs text-brandGrayText mb-1">No. Escritura</label><input type="text" id="json_no_escritura" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Notario</label><input type="text" id="json_notario" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Finca</label><input type="text" id="json_finca" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Folio</label><input type="text" id="json_folio" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Libro</label><input type="text" id="json_libro" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Área (m²)</label><input type="text" id="json_area" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div class="md:col-span-2"><label class="block text-xs text-brandGrayText mb-1">Ubicación</label><input type="text" id="json_ubicacion" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div class="md:col-span-2"><label class="block text-xs text-brandGrayText mb-1">Descripción</label><input type="text" id="json_descripcion" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Valor Comercial (Q)</label><input type="number" id="json_valor_comercial" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Titular</label><input type="text" id="json_titular" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Estatus</label><input type="text" id="json_estatus" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">No. Contrato Arrendamiento</label><input type="text" id="json_no_contrato" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Avalúo Bien</label><input type="text" id="json_avaluo" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            
        `;
    } else if (tipo === 'FIADOR') {
        fieldsHTML = `
            <!-- Asignamos fiador-search-container para forzar la flotación -->
            <div class="fiador-search-container md:col-span-2">
                <label class="block text-xs text-brandGrayText mb-1">Buscar Cliente (Fiador)</label>
                <input type="text" 
                       id="fiador_search_input" 
                       class="glass-input w-full p-2 rounded-xl text-sm" 
                       placeholder="Escriba el nombre o código..." 
                       oninput="searchSelect2('fiador')" 
                       onclick="openSelect2('fiador')" 
                       autocomplete="off">
                <input type="hidden" id="json_fiador_customer_id">
                
                <!-- Dropdown desplegable con z-index alto -->
                <div id="fiador_dropdown" class="select2-dropdown hidden"></div>
            </div>
            
            <div>
                <label class="block text-xs text-brandGrayText mb-1">Código Cliente</label>
                <input type="text" id="json_fiador_codigo" class="glass-input w-full p-2 rounded-xl text-sm bg-gray-100" readonly>
            </div>
            <div>
                <label class="block text-xs text-brandGrayText mb-1">Nombre Completo Fiador</label>
                <input type="text" id="json_fiador_nombre" class="glass-input w-full p-2 rounded-xl text-sm bg-gray-100" readonly>
            </div>
            <div>
                <label class="block text-xs text-brandGrayText mb-1">Lugar de Trabajo</label>
                <input type="text" id="json_fiador_trabajo" class="glass-input w-full p-2 rounded-xl text-sm bg-gray-100" readonly>
            </div>
            <div>
                <label class="block text-xs text-brandGrayText mb-1">Teléfono</label>
                <input type="text" id="json_fiador_tel" class="glass-input w-full p-2 rounded-xl text-sm bg-gray-100" readonly>
            </div>
            <div>
                <label class="block text-xs text-brandGrayText mb-1">Ingreso Mensual (Q)</label>
                <input type="number" id="json_fiador_ingreso" class="glass-input w-full p-2 rounded-xl text-sm bg-gray-100" readonly>
            </div>
            <input type="hidden" id="json_fiador_foto">
        `;
    } else if (tipo === 'CHEQUE / PAGARE') {
        fieldsHTML = `
            <div><label class="block text-xs text-brandGrayText mb-1">No. Cheque</label><input type="number" id="json_no_cheque" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Nombre Cuenta</label><input type="text" id="json_nombre_cuenta" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Banco</label><input type="text" id="json_banco" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Cheque Girado A</label><input type="text" id="json_girado_a" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Monto Cheque (Q)</label><input type="number" id="json_monto_cheque" class="glass-input w-full p-2 rounded-xl text-sm"></div>
        `;
    } else if (tipo === 'VEHICULO') {
        fieldsHTML = `
            <div><label class="block text-xs text-brandGrayText mb-1">Placa</label><input type="text" id="json_veh_placa" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Marca</label><input type="text" id="json_veh_marca" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Color</label><input type="text" id="json_veh_color" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">No. Chasis</label><input type="text" id="json_veh_chasis" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">No. Motor</label><input type="text" id="json_veh_motor" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Valor Comercial (Q)</label><input type="number" id="json_veh_valor" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Tarjeta Circulación</label><input type="text" id="json_veh_tarjeta" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Título</label><input type="text" id="json_veh_titulo" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">No. Póliza</label><input type="text" id="json_veh_poliza" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Monto Seguro (Q)</label><input type="number" id="json_veh_seguro" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">No. Contrato Arrendamiento</label><input type="text" id="json_veh_contrato" class="glass-input w-full p-2 rounded-xl text-sm"></div>
        `;
    } else if (tipo === 'MOBILIARIA') {
        fieldsHTML = `
            <div class="md:col-span-2"><label class="block text-xs text-brandGrayText mb-1">Descripción del Bien</label><input type="text" id="json_mob_desc" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Documento que Acredita</label><input type="text" id="json_mob_doc" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            
            <div><label class="block text-xs text-brandGrayText mb-1">No. Póliza</label><input type="text" id="json_mob_poliza" class="glass-input w-full p-2 rounded-xl text-sm"></div>
            <div><label class="block text-xs text-brandGrayText mb-1">Monto Seguro (Q)</label><input type="number" id="json_mob_seguro" class="glass-input w-full p-2 rounded-xl text-sm"></div>
        `;
    }

    container.innerHTML = fieldsHTML;
};

window.addGuaranteeDetail = function () {
    const tipo = document.getElementById('tipo_garantia').value;
    const valor = parseFloat(document.getElementById('valor_cobertura').value);

    if (isNaN(valor) || valor <= 0) {
        showToast('Ingrese un valor de cobertura válido superior a Q0.00', 'error');
        return;
    }

    let especificaciones = {};

    if (tipo === 'DERECHO DE POSESION HIPOTECA') {
        especificaciones = {
            Nombre: document.getElementById('json_nombre')?.value || "DERECHO DE POSESIÓN HIPOTECA",
            NoEscritura: document.getElementById('json_no_escritura')?.value || "",
            Notario: document.getElementById('json_notario')?.value || "",
            Area: document.getElementById('json_area')?.value || "",
            Ubicacion: document.getElementById('json_ubicacion')?.value || "",
            Descripcion: document.getElementById('json_descripcion')?.value || "",
            Valor_Comercial: parseFloat(document.getElementById('json_valor_comercial')?.value) || null,
            Titular: document.getElementById('json_titular')?.value || "",
            Estatus: document.getElementById('json_estatus')?.value || "GRAVAMEN HIPOTECARIO",
            NoContrato_de_Arrendamiento: document.getElementById('json_no_contrato')?.value || "",
            avaluoBien: document.getElementById('json_avaluo')?.value || "",
            docDigitalSoporte: document.getElementById('json_doc_soporte')?.value || ""
        };
    } else if (tipo === 'HIPOTECA') {
        especificaciones = {
            noEscritura: document.getElementById('json_no_escritura')?.value || "",
            notario: document.getElementById('json_notario')?.value || "",
            finca: document.getElementById('json_finca')?.value || "",
            folio: document.getElementById('json_folio')?.value || "",
            libro: document.getElementById('json_libro')?.value || "",
            area: document.getElementById('json_area')?.value || "",
            ubicacion: document.getElementById('json_ubicacion')?.value || "",
            descripcion: document.getElementById('json_descripcion')?.value || "",
            valor_comercial: parseFloat(document.getElementById('json_valor_comercial')?.value) || null,
            titular: document.getElementById('json_titular')?.value || "",
            estatus: document.getElementById('json_estatus')?.value || "",
            noContratoArrendamiento: document.getElementById('json_no_contrato')?.value || "",
            avaluoBien: document.getElementById('json_avaluo')?.value || "",
            docDigitalSoporte: document.getElementById('json_doc_soporte')?.value || ""
        };
    } else if (tipo === 'FIADOR') {
        especificaciones = {
            Codigo_de_Cliente: document.getElementById('json_fiador_codigo')?.value || '',
            Nombre: document.getElementById('json_fiador_nombre')?.value || '',
            Lugar_de_Trabajo: document.getElementById('json_fiador_trabajo')?.value || '',
            Ingresos: parseFloat(document.getElementById('json_fiador_ingreso')?.value) || 0,
            Numero_de_Telefono: document.getElementById('json_fiador_tel')?.value || '',
            fotografia: document.getElementById('json_fiador_foto')?.value || ''
        };
    } else if (tipo === 'CHEQUE / PAGARE') {
        especificaciones = {
            noCheque: parseInt(document.getElementById('json_no_cheque')?.value) || 0,
            NombreCuenta: document.getElementById('json_nombre_cuenta')?.value || "",
            Banco: document.getElementById('json_banco')?.value || "",
            Cheque_girado_a: document.getElementById('json_girado_a')?.value || "",
            Monto_cheque: parseFloat(document.getElementById('json_monto_cheque')?.value) || 0
        };
    } else if (tipo === 'VEHICULO') {
        especificaciones = {
            Placa: document.getElementById('json_veh_placa')?.value || "",
            Marca: document.getElementById('json_veh_marca')?.value || "",
            Color: document.getElementById('json_veh_color')?.value || "",
            NoChasis: document.getElementById('json_veh_chasis')?.value || "",
            NoMotor: document.getElementById('json_veh_motor')?.value || "",
            Valor_Comercial: parseFloat(document.getElementById('json_veh_valor')?.value) || null,
            fotografia: [],
            tarjeta_circulacion: document.getElementById('json_veh_tarjeta')?.value || "",
            titulo: document.getElementById('json_veh_titulo')?.value || "",
            NoPoliza: document.getElementById('json_veh_poliza')?.value || "",
            MontoSeguro: parseFloat(document.getElementById('json_veh_seguro')?.value) || null,
            NoContratoArrendamiento: document.getElementById('json_veh_contrato')?.value || ""
        };
    } else if (tipo === 'MOBILIARIA') {
        especificaciones = {
            DescripcionBien: document.getElementById('json_mob_desc')?.value || "",
            DocumentoAcredita: document.getElementById('json_mob_doc')?.value || "",
            imagen_documento_acredita: document.getElementById('json_mob_img_doc')?.value || "",
            fotografia_bien: document.getElementById('json_mob_foto')?.value || "",
            NoPoliza: document.getElementById('json_mob_poliza')?.value || "",
            MontoSeguro: parseFloat(document.getElementById('json_mob_seguro')?.value) || null
        };
    }

    const item = {
        id: Date.now(),
        tipo_garantia: tipo,
        valor_cobertura: valor,
        especificaciones: especificaciones,
        creation_date: new Date().toISOString()
    };

    guaranteeList.push(item);
    document.getElementById('valor_cobertura').value = '';
    renderDynamicGuaranteeFields();
    updateGuaranteeListDisplay();
    showToast('Detalle de garantía agregado correctamente.', 'success');
};

window.removeGuarantee = function(id) {
    guaranteeList = guaranteeList.filter(g => g.id !== id);
    updateGuaranteeListDisplay();
    showToast('Garantía removida.', 'info');
}

window.updateGuaranteeListDisplay = function() {
    const container = document.getElementById('garantias-list-container');
    const badge = document.getElementById('badge-garantias');
    const totalInput = document.getElementById('suma_total_garantia');
    const totalRegisteredDisplay = document.getElementById('registered-guarantee-total');

    badge.textContent = guaranteeList.length;

    let totalSuma = guaranteeList.reduce((acc, curr) => acc + curr.valor_cobertura, 0);
    totalInput.value = totalSuma.toFixed(2);
    totalRegisteredDisplay.textContent = `Q ${totalSuma.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

    if (guaranteeList.length === 0) {
        container.innerHTML = `
                    <div class="glass-card p-8 text-center text-brandGrayText rounded-xl bg-white/60">
                        <i class="fa-solid fa-folder-open text-3xl mb-2 text-brandRedDark/30"></i>
                        <p>No se han registrado detalles de garantía aún.</p>
                    </div>
                `;
        return;
    }

    container.innerHTML = guaranteeList.map((g, index) => `
                <div class="glass-card p-4 rounded-xl border-l-4 border-l-brandRed bg-white/90 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shadow-sm">
                    <div class="space-y-1">
                        <div class="flex items-center space-x-2">
                            <span class="px-2 py-0.5 text-xs font-bold bg-brandRedDark text-white rounded">${g.tipo_garantia}</span>
                            <span class="text-xs text-brandGrayText font-semibold">Ítem #${index + 1}</span>
                        </div>
                        <div class="text-xs font-mono text-darkCard bg-brandBgLight p-2 rounded-lg border border-brandGrayBorder/50">
                            <strong class="text-brandRedDark">JSON Specifications:</strong> ${JSON.stringify(g.especificaciones)}
                        </div>
                    </div>
                    <div class="flex items-center space-x-4 w-full md:w-auto justify-between md:justify-end">
                        <div class="text-right">
                            <span class="text-xs text-brandGrayText block">Valor Cobertura</span>
                            <span class="text-base font-bold text-emerald-600 font-mono">Q ${g.valor_cobertura.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
                        </div>
                        <button onclick="removeGuarantee(${g.id})" class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </div>
                </div>
            `).join('');
}