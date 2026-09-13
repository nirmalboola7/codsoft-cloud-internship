
const API_URL = "http://127.0.0.1:5000";
const statusElement = document.getElementById("status");
function showStatus(message, type = "") {

    statusElement.textContent = message;

    statusElement.className = type;
}
async function createBackup() {
    showStatus("Creating backup...", "");
    try {

        const response = await fetch(
            `${API_URL}/backup`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        if (data.success) {

            showStatus(
                `✓ Backup created successfully: ${data.backup}`,
                "success"
            );
            loadBackups();

        } else {

            showStatus(
                `✗ ${data.message}`,
                "error"
            );
        }

    } catch (error) {

        console.error("Backup error:", error);

        showStatus(
            "✗ Could not connect to Flask server.",
            "error"
        );
    }
}
async function loadBackups() {
    const backupList =
        document.getElementById("backupList");

    backupList.innerHTML =
        `<p class="loading">
            Loading backups...
        </p>`;

    try {

        const response = await fetch(
            `${API_URL}/backups`
        );

        const backups = await response.json();
        if (
            !Array.isArray(backups) ||
            backups.length === 0
        ) {

            backupList.innerHTML =
                `<p>
                    No backups found.
                </p>`;

            return;
        }
        backupList.innerHTML = "";
        backups.forEach(function(filename) {
            const item =
                document.createElement("div");

            item.className =
                "backup-item";
            const name =
                document.createElement("span");

            name.className =
                "backup-name";

            name.textContent =
                filename;
            const button =
                document.createElement("button");

            button.className =
                "restore-btn";

            button.textContent =
                "Restore";
            button.onclick = function() {

                restoreBackup(filename);

            };
            item.appendChild(name);
            item.appendChild(button);
            backupList.appendChild(item);

        });

    } catch (error) {

        console.error(
            "Backup history error:",
            error
        );

        backupList.innerHTML =
            `<p class="error">
                Could not load backup history.
            </p>`;
    }
}
async function restoreBackup(filename) {

    showStatus(
        `Restoring ${filename}...`,
        ""
    );

    try {

        const response = await fetch(
            `${API_URL}/restore/${encodeURIComponent(filename)}`,
            {
                method: "POST"
            }
        );

        const data = await response.json();


        if (data.success) {

            showStatus(
                `✓ ${filename} restored successfully.`,
                "success"
            );

        } else {

            showStatus(
                `✗ ${data.message}`,
                "error"
            );
        }

    } catch (error) {

        console.error(
            "Restore error:",
            error
        );

        showStatus(
            "✗ Restore failed. Check the Flask server.",
            "error"
        );
    }
}
window.addEventListener(
    "DOMContentLoaded",
    function() {

        loadBackups();

    }
);