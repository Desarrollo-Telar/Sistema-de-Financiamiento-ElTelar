import { urls_p } from '../API/urls_api.js';



document.addEventListener('DOMContentLoaded', () => {
    // CAMBIA ESTO: ID dinámico de tu expediente actual
    const EXPEDIENTE_ID = 1; 
    const API_URL = urls_p.api_url_documento_expediente + '?term=' + document.getElementById('expedienteId').value;

    const documentsContainer = document.getElementById('documentsContainer');
    const emptyState = document.getElementById('emptyState');
    const totalCount = document.getElementById('totalCount');
    const searchInput = document.getElementById('searchInput');
    const refreshBtn = document.getElementById('refreshBtn');

    let allDocuments = [];

    // Cargar documentos al iniciar
    fetchDocuments();

    refreshBtn.addEventListener('click', fetchDocuments);
    searchInput.addEventListener('input', filterDocuments);

    async function fetchDocuments() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error('Error al consultar los documentos');
            
            const data = await response.json();
            
            // Si la API devuelve un objeto paginado (p. ej. DRF con "results"), tomamos data.results
            allDocuments = Array.isArray(data) ? data : (data.results || []);
            renderDocuments(allDocuments);
        } catch (error) {
            console.error('Error:', error);
            documentsContainer.innerHTML = `<p style="color: red;">No se pudieron cargar los documentos.</p>`;
        }
    }

    function renderDocuments(docs) {
        totalCount.textContent = `${docs.length} archivo${docs.length !== 1 ? 's' : ''}`;
        
        if (docs.length === 0) {
            documentsContainer.style.display = 'none';
            emptyState.style.display = 'block';
            return;
        }

        emptyState.style.display = 'none';
        documentsContainer.style.display = 'grid';
        documentsContainer.innerHTML = '';

        docs.forEach(doc => {
            const fileName = getFileNameFromUrl(doc.archivo);
            const formattedDate = formatDate(doc.fecha_subida);
            const fileIcon = getFileIcon(fileName);

            const card = document.createElement('div');
            card.className = 'dm-card';
            card.innerHTML = `
                <div class="dm-card-body">
                    <div class="dm-file-icon">
                        ${fileIcon}
                    </div>
                    <div class="dm-file-info">
                        <p class="dm-file-name" title="${fileName}">${fileName}</p>
                        <p class="dm-file-date">Subido: ${formattedDate}</p>
                    </div>
                </div>
                <div class="dm-card-footer">
                    <a href="${doc.archivo}" target="_blank" rel="noopener" class="dm-link">Ver / Abrir</a>
                    <button class="dm-btn-delete" data-id="${doc.id}">Eliminar</button>
                </div>
            `;

            // Listener para eliminar archivo
            card.querySelector('.dm-btn-delete').addEventListener('click', () => deleteDocument(doc.id));
            documentsContainer.appendChild(card);
        });
    }

    function filterDocuments() {
        const query = searchInput.value.toLowerCase();
        const filtered = allDocuments.filter(doc => {
            const name = getFileNameFromUrl(doc.archivo).toLowerCase();
            return name.includes(query);
        });
        renderDocuments(filtered);
    }

    async function deleteDocument(docId) {
        if (!confirm('¿Estás seguro de que deseas eliminar este documento?')) return;

        try {
            const response = await fetch(`http://127.0.0.1:8000/documents/api/documento_expediente/${docId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });

            if (response.ok) {
                // Eliminar del array local y re-renderizar
                allDocuments = allDocuments.filter(d => d.id !== docId);
                renderDocuments(allDocuments);
            } else {
                alert('No se pudo eliminar el archivo.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al intentar eliminar.');
        }
    }

    // --- Funciones auxiliares ---

    function getFileNameFromUrl(url) {
        if (!url) return 'Archivo sin nombre';
        return url.split('/').pop().split('?')[0];
    }

    function formatDate(isoString) {
        if (!isoString) return '';
        const date = new Date(isoString);
        return date.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: 'short',
            year: 'numeric'
        });
    }

    function getFileIcon(fileName) {
        const ext = fileName.split('.').pop().toLowerCase();
        
        // Ícono para PDFs
        if (ext === 'pdf') {
            return `<svg viewBox="0 0 24 24" fill="#ef4444"><path d="M20 2H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-8.5 7.5c0 .83-.67 1.5-1.5 1.5H9v2H7.5V7H10c.83 0 1.5.67 1.5 1.5v1zm5 2c0 .83-.67 1.5-1.5 1.5h-2.5V7H15c.83 0 1.5.67 1.5 1.5v3zm4-3H19v1h1.5V11H19v2h-1.5V7h3v1.5z"/></svg>`;
        } 
        // Ícono para Imágenes
        if (['jpg', 'jpeg', 'png', 'webp'].includes(ext)) {
            return `<svg viewBox="0 0 24 24" fill="#3b82f6"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg>`;
        }
        // Ícono por defecto (Word, Excel, genérico)
        return `<svg viewBox="0 0 24 24" fill="#64748b"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>`;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});