document.addEventListener('DOMContentLoaded', function() {
    const parallelUploadsInput = document.getElementById('parallel-uploads');

    parallelUploadsInput.addEventListener('change', function() {
        // TODO: Implement logic to handle parallel uploads configuration
    });

    const fileInput = document.getElementById('file-input');
    const fileListBody = document.getElementById('file-list-body');

    fileInput.addEventListener('change', function() {
        fileListBody.innerHTML = ''; // Clear the current file list

        Array.from(fileInput.files).forEach(file => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${file.name}</td>
                <td>${file.size} bytes</td>
                <td>Not available</td>
                <td>Ready to upload</td>
                <td><progress value="0" max="100"></progress></td>
            `;
            fileListBody.appendChild(row);
        });
    });
});
