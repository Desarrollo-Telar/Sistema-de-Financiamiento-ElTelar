const sidebar = document.getElementById('sidebar');
const navbar_comp = document.getElementById('navbar_comp');
const navbar_respo = document.getElementById('navbar_respo');
function toggleSidebarVisibility() {
  if (window.innerWidth <= 768) {
    sidebar.classList.add('d-none');
    navbar_comp.classList.add('d-none');
    navbar_respo.classList.remove('d-none');
  } else {
    sidebar.classList.remove('d-none');
    navbar_comp.classList.remove('d-none');
    navbar_respo.classList.add('d-none');
  }
}

// Ejecutar al cargar la página
toggleSidebarVisibility();

// Escuchar cuando la ventana cambia de tamaño
window.addEventListener('resize', toggleSidebarVisibility);
