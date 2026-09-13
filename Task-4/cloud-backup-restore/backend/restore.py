import os
import zipfile
def restore_backup(backup_path, restore_folder):
    if not os.path.exists(backup_path):
        print("Backup file does not exist.")
        return False
    os.makedirs(restore_folder, exist_ok=True)
    with zipfile.ZipFile(backup_path, "r") as zip_file:
        zip_file.extractall(restore_folder)

    print(f"Backup restored successfully to: {restore_folder}")

    return True