from flask import Flask, jsonify, send_from_directory
import os
from apscheduler.schedulers.background import BackgroundScheduler
from backup import create_backup
from restore import restore_backup
from cloud_storage import upload_backup, download_backup
app = Flask(__name__)
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SOURCE_FOLDER = os.path.join(
    BASE_DIR,
    "files"
)

BACKUP_FOLDER = os.path.join(
    BASE_DIR,
    "backups"
)

RESTORE_FOLDER = os.path.join(
    BASE_DIR,
    "restored"
)

FRONTEND_FOLDER = os.path.join(
    BASE_DIR,
    "frontend"
)
@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_FOLDER,
        "index.html"
    )
@app.route("/<path:filename>")
def frontend_files(filename):

    return send_from_directory(
        FRONTEND_FOLDER,
        filename
    )
@app.route("/backup", methods=["POST"])
def backup():

    backup_path = create_backup(
        SOURCE_FOLDER,
        BACKUP_FOLDER
    )

    if backup_path is None:

        return jsonify({
            "success": False,
            "message": "Source folder does not exist"
        }), 400

    try:

        cloud_file = upload_backup(
            backup_path
        )

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Local backup created, but S3 upload failed",
            "error": str(e)
        }), 500

    return jsonify({

        "success": True,

        "message":
            "Backup created and uploaded successfully",

        "backup":
            os.path.basename(backup_path),

        "cloud_file":
            cloud_file
    })
@app.route("/backups", methods=["GET"])
def list_backups():

    if not os.path.exists(BACKUP_FOLDER):

        return jsonify([])

    backups = []

    for filename in os.listdir(BACKUP_FOLDER):

        if filename.endswith(".zip"):

            backups.append(filename)

    backups.sort(reverse=True)

    return jsonify(backups)
@app.route("/restore/<filename>", methods=["POST"])
def restore(filename):

    if not filename.endswith(".zip"):

        return jsonify({
            "success": False,
            "message": "Invalid backup file"
        }), 400

    try:

        downloaded_file = download_backup(
            filename,
            BACKUP_FOLDER
        )

        success = restore_backup(
            downloaded_file,
            RESTORE_FOLDER
        )

        if not success:

            return jsonify({
                "success": False,
                "message": "Backup could not be restored"
            }), 500

        return jsonify({

            "success": True,

            "message":
                "Backup downloaded from S3 and restored successfully",

            "backup":
                filename,

            "restored_to":
                RESTORE_FOLDER
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message":
                "Cloud restore failed",

            "error":
                str(e)
        }), 500
def automatic_backup():

    print("Starting automatic backup...")

    backup_path = create_backup(
        SOURCE_FOLDER,
        BACKUP_FOLDER
    )

    if backup_path is None:

        print(
            "Automatic backup failed: "
            "source folder does not exist"
        )

        return

    try:

        cloud_file = upload_backup(
            backup_path
        )

        print(
            "Automatic backup uploaded successfully: "
            f"{cloud_file}"
        )

    except Exception as e:

        print(
            f"Automatic S3 upload failed: {e}"
        )
scheduler = BackgroundScheduler()

scheduler.add_job(
    automatic_backup,
    "interval",
    hours=1
)

scheduler.start()
if __name__ == "__main__":

    try:

        app.run(
            host="127.0.0.1",
            port=5000,
            debug=True,
            use_reloader=False
        )

    finally:

        scheduler.shutdown()