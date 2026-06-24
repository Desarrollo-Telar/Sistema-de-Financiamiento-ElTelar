import {postLaboral} from '../API/workinginformation/post_api.js';
import {postDireccion} from '../API/address/post_api.js';

async function guardar_informacion_laboral(cliente){
  let formData = new FormData();

  let position = document.getElementById('cargo').value;
  let company_name  = document.getElementById('empresa').value;
  let start_date = document.getElementById('fechaIngreso').value;
  let description  = document.getElementById('description').value;
  let salary = document.getElementById('salario').value;
  let working_hours  = document.getElementById('working_hours').value;
  let phone_number = document.getElementById('telefonoEmpresa').value;
  let source_of_income  = document.getElementById('tipoContrato').value;
  let employment_status = document.getElementById('employment_status').value;

  formData.append('customer_id', cliente )
  formData.append('position', position )
  formData.append('company_name', company_name )
  formData.append('start_date', start_date )
  formData.append('description', description )
  formData.append('salary', salary )
  formData.append('working_hours', working_hours )
  formData.append('phone_number', phone_number )
  formData.append('source_of_income', source_of_income )
  formData.append('employment_status', employment_status )

  return await postLaboral(formData);
}

async function guardar_direccion_laboral(cliente, subsidiary){
  let formData = new FormData();

  let street = document.getElementById('direccionCompleta').value;
  let number  = document.getElementById('zona').value;
  let city = document.getElementById('departamento').value;
  let state  = document.getElementById('municipio').value;
  let latitud = document.getElementById('latitud').value;
  let longitud  = document.getElementById('longitud').value;

  formData.append('type_address', 'Dirección de Trabajo' )
  formData.append('customer_id', cliente )
  formData.append('subsidiary', subsidiary )
  formData.append('country', 'GUATEMALA' )

  formData.append('street', street )
  formData.append('number', number )
  formData.append('city', city )
  formData.append('state', state )  
  formData.append('latitud', latitud )
  formData.append('longitud', longitud )

  return await postDireccion(formData);
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registroForm");
  const sections = Array.from(document.querySelectorAll("[data-section]"));
  const railSteps = Array.from(document.querySelectorAll(".rail__step"));
  const progressFill = document.getElementById("progressFill");
  const progressValue = document.getElementById("progressValue");
  const summary = document.getElementById("summary");
  const summaryList = document.getElementById("summaryList");
  const editAgainBtn = document.getElementById("editAgain");

  // CORREGIDO: 'document' en minúsculas
  let cliente = document.getElementById('customer_id').value;
  let subsidiary = document.getElementById('subsidiary').value;

  const FIELD_LABELS = {
    empresa: "Empresa",
    cargo: "Cargo o puesto",
    tipoContrato: "Tipo de contrato",
    fechaIngreso: "Fecha de ingreso",
    salario: "Salario mensual",
    telefonoEmpresa: "Teléfono de la empresa",
    employment_status: "Estado Laboral",
    nombreJefe: "Jefe inmediato",
    departamento: "Departamento",
    municipio: "Municipio",
    zona: "Zona / colonia",
    codigoPostal: "Código postal",
    direccionCompleta: "Dirección",
    referencia: "Punto de referencia",
  };

  const CONTRATO_LABELS = {
    indefinido: "Indefinido",
    temporal: "Temporal",
    por_servicios: "Por servicios profesionales",
    independiente: "Independiente",
  };

  function validateField(field) {
    const value = field.value.trim();
    let message = "";

    if (field.hasAttribute("required") && !value) {
      message = "Este campo es obligatorio.";
    }  else if (field.type === "tel" && value && !/^[0-9+\s()-]{7,15}$/.test(value)) {
      message = "Ingresa un teléfono válido.";
    } else if (field.type === "number" && value && Number(value) < 0) {
      message = "El valor no puede ser negativo.";
    } else if (field.id === "fechaIngreso" && value) {
      const fecha = new Date(value);
      if (fecha > new Date()) {
        message = "La fecha no puede ser futura.";
      }
    }

    setFieldError(field, message);
    return !message;
  }

  function setFieldError(field, message) {
    const errorEl = document.querySelector(`[data-error-for="${field.id}"]`);
    if (errorEl) errorEl.textContent = message;
    field.classList.toggle("is-invalid", Boolean(message));
  }

  // ... (Tus funciones validateSection, goToSection y observers se mantienen igual)
  function validateSection(section) {
    const fields = section.querySelectorAll("input, select, textarea");
    let valid = true;
    fields.forEach((field) => {
      if (!validateField(field)) valid = false;
    });
    return valid;
  }

  form.querySelectorAll("input, select, textarea").forEach((field) => {
    field.addEventListener("blur", () => validateField(field));
    field.addEventListener("input", () => {
      if (field.classList.contains("is-invalid")) validateField(field);
    });
  });

  function goToSection(targetId) {
    const target = document.getElementById(targetId);
    if (!target) return;
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  document.querySelectorAll("[data-next]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const currentSection = btn.closest("[data-section]");
      if (validateSection(currentSection)) {
        goToSection(btn.dataset.next);
      } else {
        currentSection.querySelector(".is-invalid")?.focus();
      }
    });
  });

  document.querySelectorAll("[data-prev]").forEach((btn) => {
    btn.addEventListener("click", () => goToSection(btn.dataset.prev));
  });

  railSteps.forEach((step) => {
    step.addEventListener("click", () => goToSection(step.dataset.target));
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          railSteps.forEach((step) => {
            step.classList.toggle("is-active", step.dataset.target === entry.target.id);
          });
        }
      });
    },
    { rootMargin: "-30% 0px -55% 0px" }
  );
  sections.forEach((section) => observer.observe(section));

  function updateProgress() {
    const fields = Array.from(form.querySelectorAll("input, select, textarea"));
    const required = fields.filter((f) => f.hasAttribute("required"));
    const filled = required.filter((f) => f.value.trim() !== "");
    const percent = required.length ? Math.round((filled.length / required.length) * 100) : 0;
    progressFill.style.width = `${percent}%`;
    progressValue.textContent = `${percent}%`;
  }

  form.addEventListener("input", updateProgress);
  form.addEventListener("change", updateProgress);
  updateProgress();

  // CORREGIDO: Agregado 'async' aquí abajo para soportar await
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      let formValid = true;
      sections.forEach((section) => {
        if (!validateSection(section)) formValid = false;
      });

      if (!formValid) {
        const firstInvalid = form.querySelector(".is-invalid");
        if (firstInvalid) {
          firstInvalid.closest("[data-section]").scrollIntoView({ behavior: "smooth", block: "start" });
          firstInvalid.focus();
        }
        return;
      }

      const data = Object.fromEntries(new FormData(form).entries());
      
      // Llamadas asíncronas correctas
      await guardar_informacion_laboral(cliente);
      await guardar_direccion_laboral(cliente, subsidiary);

      showSummary(data);
      console.log("Registro laboral guardado:", data);

    } catch (error) {
      console.error('Error al registrar los datos:', error);
      // ... Tu manejo de errores de SweetAlert se mantiene igual
      if (error.response) {
          console.error('Error en la respuesta del servidor:', error.response.data);
          Swal.fire({
              icon: "error",
              title: `Error ${error.response.status}`,
              text: error.response.data.message || 'Ocurrió un problema en el servidor.',
              timer: 10000,
              showConfirmButton: false,
          });
      } else if (error.request) {
          console.error('Error en la solicitud:', error.request);
          Swal.fire({
              icon: "error",
              title: `Sin respuesta del servidor`,
              text: `No se obtuvo respuesta del servidor. Por favor, inténtalo más tarde.`,
              timer: 10000,
              showConfirmButton: false,
          });
      } else {
          console.error('Error:', error.message);
          Swal.fire({
              icon: "error",
              title: `Error inesperado`,
              text: error.message,
              timer: 10000,
              showConfirmButton: false,
          });
      }

      summary.hidden = true;
      form.hidden = false;
      goToSection("laboral");
    }
  });

  function showSummary(data) {
    summaryList.innerHTML = "";

    Object.entries(data).forEach(([key, rawValue]) => {
      if (!rawValue) return;

      let value = rawValue;
      if (key === "tipoContrato") value = CONTRATO_LABELS[rawValue] || rawValue;
      if (key === "salario") value = `Q ${Number(rawValue).toLocaleString("es-GT", { minimumFractionDigits: 2 })}`;
      if (key === "fechaIngreso") value = new Date(rawValue + "T00:00:00").toLocaleDateString("es-GT");

      const dt = document.createElement("dt");
      dt.textContent = FIELD_LABELS[key] || key;
      const dd = document.createElement("dd");
      dd.textContent = value;

      summaryList.append(dt, dd);
    });

    form.hidden = true;
    summary.hidden = false;
    summary.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  editAgainBtn.addEventListener("click", () => {
    summary.hidden = true;
    form.hidden = false;
    goToSection("laboral");
  });
});