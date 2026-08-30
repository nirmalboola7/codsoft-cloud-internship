async function uploadFile() {

    const fileInput = document.getElementById("fileInput");

    const result = document.getElementById("result");


    if (fileInput.files.length === 0) {

        result.innerText = "Please select a file.";

        return;
    }


    const file = fileInput.files[0];

    const formData = new FormData();

    formData.append("file", file);


    result.innerText = "Uploading...";


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/upload",
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        result.innerText =
            data.message +
            "\nFilename: " + (data.filename || file.name) +
            "\nSize: " + (data.size || file.size) + " bytes" +
            "\nHash: " + data.hash;


        loadStatistics();

    }


    catch (error) {

        console.error(error);

        result.innerText =
            "Error connecting to backend.";

    }

}


async function loadStatistics() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/stats"
        );


        const data = await response.json();


        document.getElementById("uniqueFiles").innerText =
            data.unique_files;


        document.getElementById("uploadAttempts").innerText =
            data.upload_attempts;


        document.getElementById("duplicatesBlocked").innerText =
            data.duplicates_blocked;


        document.getElementById("storageUsed").innerText =
            data.storage_used + " bytes";


        document.getElementById("storageSaved").innerText =
            data.storage_saved + " bytes";

    }


    catch (error) {

        console.error(error);

    }

}


loadStatistics();