
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const emptyState = document.getElementById('emptyState');
const fileCount = document.getElementById('fileCount');

let uploadedFiles = [];

dropzone.addEventListener('click', () => fileInput.click());

['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add('active');
    });
});

['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove('active');
    });
});

dropzone.addEventListener('drop', (e) => {
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
});

fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files);
    handleFiles(files);
    fileInput.value = '';
});

function handleFiles(files) {
    files.forEach(file => {
        const fileObj = {
            id: Date.now() + Math.random().toString(36).substr(2, 9),
            file: file,
            url: URL.createObjectURL(file)
        };
        uploadedFiles.push(fileObj);
    });
    renderFileList();
}

function renderFileList() {
    fileCount.textContent = uploadedFiles.length;

    if (uploadedFiles.length === 0) {
        emptyState.style.display = 'block';
        fileList.innerHTML = '';
        fileList.appendChild(emptyState);
        return;
    }

    emptyState.style.display = 'none';
    fileList.innerHTML = '';

    uploadedFiles.forEach(item => {
        const li = document.createElement('li');
        li.className = 'file-item';

        li.innerHTML = `
          <div class="file-info">
            <svg class="file-icon" viewBox="0 0 24 24">
              <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
            </svg>
            <div class="file-details">
              <span class="file-name" title="${item.file.name}">${item.file.name}</span>
              <span class="file-size">${formatFileSize(item.file.size)}</span>
            </div>
          </div>
          <div class="file-actions">
            <a href="${item.url}" target="_blank" class="btn-action btn-view">Ver / Abrir</a>
            <button class="btn-action btn-delete" onclick="deleteFile('${item.id}')">Eliminar</button>
          </div>
        `;

        fileList.appendChild(li);
    });
}

function deleteFile(id) {
    const fileIndex = uploadedFiles.findIndex(f => f.id === id);
    if (fileIndex !== -1) {
        URL.revokeObjectURL(uploadedFiles[fileIndex].url);
        uploadedFiles.splice(fileIndex, 1);
        renderFileList();
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
