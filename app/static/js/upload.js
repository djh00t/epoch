document.addEventListener('DOMContentLoaded', function() {
    const parallelUploadsInput = document.getElementById('parallel-uploads');
    const fileInput = document.getElementById('file-input');
    const fileListBody = document.getElementById('file-list-body');
    const uploadForm = document.querySelector('form');

    parallelUploadsInput.addEventListener('change', function() {
        // TODO: Implement logic to handle parallel uploads configuration
    });

    const fileInput = document.getElementById('file-input');
    const fileListBody = document.getElementById('file-list-body');

    fileInput.addEventListener('change', function() {
        fileListBody.innerHTML = ''; // Clear the current file list

        Array.from(fileInput.files).forEach(file => {
        Array.from(fileInput.files).forEach((file, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${file.name}</td>
                <td>${file.size} bytes</td>
                <td>Not available</td>
                <td>Ready to upload</td>
                <td><progress id="progress_${index}" value="0" max="100"></progress></td>
                <td><progress value="0" max="100"></progress></td>
            `;
            fileListBody.appendChild(row);
        });
    });

    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        uploadFiles(fileInput.files);
    });

    function uploadFiles(files) {
        const formData = new FormData();
        Array.from(files).forEach(file => {
            formData.append('files[]', file, file.name);
        });

        const xhr = new XMLHttpRequest();
        xhr.open('POST', uploadForm.action, true);

        xhr.upload.onprogress = function(event) {
            if (event.lengthComputable) {
                const percentComplete = Math.round((event.loaded / event.total) * 100);
                Array.from(files).forEach((file, index) => {
                    const progress = document.getElementById(`progress_${index}`);
                    progress.value = percentComplete;
                });
            }
        };

        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log('Upload complete!');
                // Update the UI to reflect that the upload is complete
                Array.from(files).forEach((file, index) => {
                    const statusCell = document.getElementById(`status_${index}`);
                    if (statusCell) {
                        statusCell.textContent = 'Upload complete';
                    }
                });
            } else {
                console.error('Upload failed.');
                // Handle upload failure here
            }
        };

        // Prevent the page from navigating away after the upload
        xhr.onloadend = function() {
            // Update the UI or notify the user as needed
        };

        xhr.send(formData);
    }
});
function createThumbnail(file, callback) {
    const reader = new FileReader();
    reader.onload = function (e) {
        const img = document.createElement("img");
        img.src = e.target.result;
        img.onload = function () {
            const canvas = document.createElement("canvas");
            const ctx = canvas.getContext("2d");
            const maxW = 100;
            const maxH = 100;
            let width = img.width;
            let height = img.height;

            if (width > height) {
                if (width > maxW) {
                    height *= maxW / width;
                    width = maxW;
                }
            } else {
                if (height > maxH) {
                    width *= maxH / height;
                    height = maxH;
                }
            }
            canvas.width = width;
            canvas.height = height;
            ctx.drawImage(img, 0, 0, width, height);
            callback(canvas.toDataURL("image/jpeg", 0.7));
        };
    };
    reader.readAsDataURL(file);
}

// Modify the existing file input change event listener to create thumbnails
fileInput.addEventListener('change', function() {
    fileListBody.innerHTML = ''; // Clear the current file list

    Array.from(fileInput.files).forEach((file, index) => {
        createThumbnail(file, function(thumbnailDataUrl) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${file.name}</td>
                <td>${file.size} bytes</td>
                <td><img src="${thumbnailDataUrl}" class="thumbnail"></td>
                <td>Ready to upload</td>
                <td><progress value="0" max="100"></progress></td>
            `;
            fileListBody.appendChild(row);
        });
    });
});
