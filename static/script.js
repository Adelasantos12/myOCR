document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const processBtn = document.getElementById('process-btn');
    const uploadAreaContent = uploadArea.querySelector('.upload-area-content p');

    const statusArea = document.getElementById('status-area');
    const resultsArea = document.getElementById('results-area');
    const errorArea = document.getElementById('error-area');

    const extractedText = document.getElementById('extracted-text');
    const downloadTxt = document.getElementById('download-txt');
    const downloadDocx = document.getElementById('download-docx');
    const errorMessage = document.getElementById('error-message');

    let selectedFile = null;

    // --- UI State Management ---
    function showState(state) {
        // Hide all dynamic sections first
        statusArea.style.display = 'none';
        resultsArea.style.display = 'none';
        errorArea.style.display = 'none';
        uploadArea.style.display = 'block'; // Show upload by default
        processBtn.style.display = 'block'; // Show process button by default

        switch (state) {
            case 'processing':
                uploadArea.style.display = 'none';
                processBtn.style.display = 'none';
                statusArea.style.display = 'block';
                break;
            case 'success':
                uploadArea.style.display = 'none';
                processBtn.style.display = 'none';
                resultsArea.style.display = 'block';
                break;
            case 'error':
                // In case of error, we show the error message but also keep the upload UI visible
                // so the user can try again easily.
                errorArea.style.display = 'block';
                break;
            case 'default':
            default:
                // All sections hidden, upload area and button visible
                break;
        }
    }

    // --- File Handling and Upload Area Interactions ---
    uploadArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) handleFile(fileInput.files[0]);
    });

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.classList.add('drag-over');
            uploadAreaContent.textContent = 'Drop the file to upload';
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.classList.remove('drag-over');
            resetUploadText();
        }, false);
    });

    uploadArea.addEventListener('drop', (e) => {
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    function handleFile(file) {
        if (file && file.type === 'application/pdf') {
            selectedFile = file;
            uploadAreaContent.textContent = selectedFile.name;
            processBtn.disabled = false;
            showState('default'); // Clear any previous error messages
        } else {
            selectedFile = null;
            errorMessage.textContent = 'Invalid file type. Please select a PDF.';
            showState('error');
            processBtn.disabled = true;
        }
    }

    function resetUploadText() {
        uploadAreaContent.textContent = selectedFile ? selectedFile.name : 'Drag and drop your PDF here, or click to select a file';
    }


    // --- Form Submission ---
    processBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        showState('processing');
        processBtn.disabled = true;

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.status === 'SUCCESS') {
                extractedText.value = result.text;
                downloadTxt.href = `/download/${result.txt_path}`;
                downloadDocx.href = `/download/${result.docx_path}`;
                showState('success');
            } else {
                errorMessage.textContent = result.message || 'An unknown error occurred.';
                showState('error');
                processBtn.disabled = false; // Re-enable on error
            }
        } catch (error) {
            errorMessage.textContent = 'A network error occurred. Please try again.';
            showState('error');
            processBtn.disabled = false; // Re-enable on error
            console.error('Error:', error);
        }
    });

    // Initialize with default state
    showState('default');
});
