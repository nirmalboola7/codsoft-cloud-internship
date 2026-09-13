import os
import zipfile
from datetime import datetime
def create_backup(source_folder, backup_folder):
    if not os.path.exists(source_folder):
        print("Source folder does not exist.")
        return None
    os.makedirs(backup_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"backup_{timestamp}.zip"

    backup_path = os.path.join(backup_folder, backup_name)


    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, directories, files in os.walk(source_folder):

            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, source_folder)

                zip_file.write(file_path, relative_path)

    print(f"Backup created successfully: {backup_path}")

    return backup_path