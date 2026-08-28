
const API_URL = "http://127.0.0.1:5000";


// --------------------------------------------------
// GET HTML ELEMENTS
// --------------------------------------------------

const fileInput = document.getElementById("fileInput");

const uploadButton = document.getElementById("uploadButton");

const refreshButton = document.getElementById("refreshButton");

const message = document.getElementById("message");

const fileList = document.getElementById("fileList");


// --------------------------------------------------
// UPLOAD FILE
// --------------------------------------------------

async function uploadFile() {

    // Check if user selected a file
    if (fileInput.files.length === 0) {

        message.innerText = "❌ Please select a file.";

        return;
    }


    const file = fileInput.files[0];


    // Create FormData
    const formData = new FormData();

    formData.append("file", file);


    // Show uploading message
    message.innerText = "⏳ Uploading...";


    try {

       const response = await fetch(
            `${API_URL}/upload`,
            {
                method: "POST",
                body: formData
            }
        );


        const result = await response.json();


        if (response.ok) {

            message.innerText =
                "✅ " + result.message;


            // Clear file input
            fileInput.value = "";


            // Refresh file list
            loadFiles();

        } else {

            message.innerText =
                "❌ " + result.error;

        }


    } catch (error) {

        message.innerText =
            "❌ Could not connect to backend.";

        console.error(error);

    }

}


// --------------------------------------------------
// LOAD FILES
// --------------------------------------------------

async function loadFiles() {

    fileList.innerHTML =
        '<p class="loading">Loading files...</p>';


    try {

        const response = await fetch(
            `${API_URL}/files`
        );


        const files = await response.json();


        // Clear existing files
        fileList.innerHTML = "";


        // No files
        if (files.length === 0) {

            fileList.innerHTML =
                '<p class="loading">No files uploaded yet.</p>';

            return;

        }


        // Display every file
        files.forEach(file => {

            const fileItem =
                document.createElement("div");

            fileItem.className = "file-item";


            // File information
            const fileInfo =
                document.createElement("div");

            fileInfo.className = "file-info";


            const fileName =
                document.createElement("div");

            fileName.className = "file-name";

            fileName.innerText =
                "📄 " + file.name;


            const fileSize =
                document.createElement("div");

            fileSize.className = "file-size";

            fileSize.innerText =
                formatFileSize(file.size);


            fileInfo.appendChild(fileName);

            fileInfo.appendChild(fileSize);


            // Buttons
            const actions =
                document.createElement("div");

            actions.className = "file-actions";


            // Download button
            const downloadButton =
                document.createElement("button");

            downloadButton.className =
                "download-button";

            downloadButton.innerText =
                "Download";


            downloadButton.onclick =
                function () {

                    downloadFile(file.name);

                };


            // Delete button
            const deleteButton =
                document.createElement("button");

            deleteButton.className =
                "delete-button";

            deleteButton.innerText =
                "Delete";


            deleteButton.onclick =
                function () {

                    deleteFile(file.name);

                };


            actions.appendChild(downloadButton);

            actions.appendChild(deleteButton);


            // Add everything
            fileItem.appendChild(fileInfo);

            fileItem.appendChild(actions);


            fileList.appendChild(fileItem);

        });


    } catch (error) {

        fileList.innerHTML =
            '<p class="loading">❌ Could not load files.</p>';

        console.error(error);

    }

}


// --------------------------------------------------
// DOWNLOAD FILE
// --------------------------------------------------

function downloadFile(filename) {

    const encodedFilename =
        encodeURIComponent(filename);


    const downloadURL =
        `${API_URL}/download/${encodedFilename}`;


    window.location.href =
        downloadURL;

}


// --------------------------------------------------
// DELETE FILE
// --------------------------------------------------

async function deleteFile(filename) {

    const confirmed =
        confirm(
            `Are you sure you want to delete "${filename}"?`
        );


    if (!confirmed) {

        return;

    }


    try {

        const response = await fetch(

            `${API_URL}/delete/${encodeURIComponent(filename)}`,

            {
                method: "DELETE"
            }

        );


        const result =
            await response.json();


        if (response.ok) {

            message.innerText =
                "✅ " + result.message;


            // Refresh file list
            loadFiles();

        } else {

            message.innerText =
                "❌ " + result.error;

        }


    } catch (error) {

        message.innerText =
            "❌ Could not connect to backend.";

        console.error(error);

    }

}


// --------------------------------------------------
// FORMAT FILE SIZE
// --------------------------------------------------

function formatFileSize(bytes) {

    if (bytes < 1024) {

        return bytes + " B";

    }


    if (bytes < 1024 * 1024) {

        return (
            (bytes / 1024).toFixed(2)
            + " KB"
        );

    }


    return (
        (bytes / (1024 * 1024)).toFixed(2)
        + " MB"
    );

}


// --------------------------------------------------
// BUTTON EVENTS
// --------------------------------------------------

uploadButton.addEventListener(
    "click",
    uploadFile
);


refreshButton.addEventListener(
    "click",
    loadFiles
);


// --------------------------------------------------
// LOAD FILES WHEN PAGE OPENS
// --------------------------------------------------

loadFiles();