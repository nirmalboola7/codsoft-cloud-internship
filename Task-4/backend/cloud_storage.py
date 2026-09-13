import boto3
import os
BUCKET_NAME = "cloud-backup-restore-nirmal-2026"

s3 = boto3.client("s3")
def upload_backup(file_path):

    file_name = os.path.basename(file_path)

    s3.upload_file(
        file_path,
        BUCKET_NAME,
        file_name
    )

    print(f"Backup uploaded to S3: {file_name}")

    return file_name
def download_backup(file_name, download_folder):
    os.makedirs(download_folder, exist_ok=True)
    download_path = os.path.join(
        download_folder,
        file_name
    )
    s3.download_file(
        BUCKET_NAME,
        file_name,
        download_path
    )

    print(f"Backup downloaded from S3: {file_name}")

    return download_path