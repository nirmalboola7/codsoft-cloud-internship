# ☁️ Cloud Backup & Restore System

A cloud-based backup and restore application that automatically creates compressed backups of local files, uploads them to **Amazon S3**, maintains backup history, and allows users to restore previous backups.

---

## 📌 Project Overview

The **Cloud Backup & Restore System** is designed to protect important local files by creating compressed ZIP backups and storing them securely in Amazon S3 cloud storage.

The system provides:

* Local file backup
* ZIP compression
* Cloud upload using Amazon S3
* Backup history
* Restore previous backups
* Automatic scheduled backups
* Simple web-based dashboard

---

## 🎯 Objectives

The main objectives of this project are:

1. Automatically back up local files.
2. Compress files before uploading to reduce storage usage.
3. Store backups securely in Amazon S3.
4. Maintain a history of available backups.
5. Allow users to restore previous backups.
6. Schedule automatic backups periodically.
7. Provide a simple and attractive web interface.

---

## 🏗️ Project Architecture

```text
                 ┌──────────────────────┐
                 │      User / Browser  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Flask Web App     │
                 │       app.py         │
                 └──────────┬───────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        ┌───────────┐ ┌───────────┐ ┌─────────────┐
        │  Backup   │ │  Restore  │ │  Scheduler  │
        │  Module   │ │  Module   │ │ APScheduler │
        └─────┬─────┘ └─────┬─────┘ └─────────────┘
              │             │
              ▼             ▼
        ┌─────────────────────────┐
        │    Cloud Storage        │
        │       Amazon S3         │
        └─────────────────────────┘
```

---

## 📁 Project Structure

```text
cloud-backup-restore/
│
├── README.md
│
├── backend/
│   ├── app.py
│   ├── backup.py
│   ├── restore.py
│   ├── cloud_storage.py
│   └── requirements.txt
│
├── files/
│   └── test.txt
│
├── backups/
│
├── restored/
│
└── frontend/
    ├── index.html
    ├── script.js
    └── style.css
```

---

## 🛠️ Technologies Used

### Backend

* Python
* Flask
* Boto3
* APScheduler

### Cloud

* Amazon Web Services (AWS)
* Amazon S3

### Frontend

* HTML
* CSS
* JavaScript

### Other

* ZIP compression
* REST API
* Git & GitHub

---

## ☁️ AWS Service Used

### Amazon S3

Amazon S3 is used as the cloud storage service for storing backup ZIP files.

Example:

```text
Local Files
     ↓
ZIP Compression
     ↓
Backup ZIP
     ↓
Boto3
     ↓
Amazon S3
```

The S3 bucket used for this project is:

```text
cloud-backup-restore-nirmal-2026
```

AWS Region:

```text
ap-south-1
```

---

## 🔄 How the System Works

### 1. User Creates a Backup

The user clicks:

```text
Create Backup
```

The frontend sends a request to:

```text
POST /backup
```

---

### 2. Files Are Compressed

The backend scans the `files/` folder.

Example:

```text
files/
└── test.txt
```

The system creates:

```text
backups/
└── backup_2026-09-12_18-54-00.zip
```

ZIP compression is used to reduce the amount of storage required.

---

### 3. Backup Is Uploaded to AWS S3

The compressed ZIP file is uploaded using **Boto3**.

```text
Local Backup
     ↓
Boto3
     ↓
Amazon S3
```

---

### 4. Backup History

The application provides a backup history through:

```text
GET /backups
```

The system displays available `.zip` backup files.

---

### 5. Restore a Backup

When the user selects:

```text
Restore
```

the frontend sends:

```text
POST /restore/<filename>
```

The backend:

```text
Amazon S3
     ↓
Download ZIP
     ↓
Extract ZIP
     ↓
restored/
```

The restored files are placed inside:

```text
restored/
```

---

## ⏰ Automatic Backup

The project uses **APScheduler** for periodic backups.

Current configuration:

```python
scheduler.add_job(
    automatic_backup,
    "interval",
    hours=1
)
```

This means the application automatically creates and uploads a backup every **1 hour** while the Flask application is running.

The automatic process is:

```text
Scheduler
    ↓
Create ZIP Backup
    ↓
Upload to S3
    ↓
Backup Stored in Cloud
```

---

## 🌐 API Endpoints

| Method | Endpoint              | Purpose                  |
| ------ | --------------------- | ------------------------ |
| GET    | `/`                   | Open web application     |
| POST   | `/backup`             | Create and upload backup |
| GET    | `/backups`            | View backup history      |
| POST   | `/restore/<filename>` | Restore a backup         |

---

## 📡 Example Backup Response

After successfully creating a backup:

```json
{
    "success": true,
    "message": "Backup created and uploaded successfully",
    "backup": "backup_2026-09-12_18-54-00.zip",
    "cloud_file": "backup_2026-09-12_18-54-00.zip"
}
```

---

## 💻 Installation

### Step 1: Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project:

```bash
cd cloud-backup-restore
```

---

### Step 2: Install Python Dependencies

Move into the backend:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📦 Requirements

The `requirements.txt` file contains:

```text
Flask
boto3
APScheduler
flask-cors
```

---

## 🔐 AWS Configuration

Configure AWS CLI before running the application:

```bash
aws configure
```

Enter your:

```text
AWS Access Key ID
AWS Secret Access Key
Default region: ap-south-1
Output format: json
```

Verify the AWS configuration:

```bash
aws sts get-caller-identity
```

The command should return your AWS account information.

---

## ▶️ Run the Application

From the `backend` directory:

```bash
python app.py
```

The Flask server will start at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

## 🖥️ Using the Application

### Create Backup

1. Open the application.
2. Click **Create Backup**.
3. The system scans the `files/` folder.
4. A ZIP backup is created.
5. The ZIP file is uploaded to Amazon S3.
6. The backup appears in Backup History.

### Restore Backup

1. Open Backup History.
2. Select a backup.
3. Click **Restore**.
4. The backup is downloaded from S3.
5. The ZIP file is extracted.
6. Restored files appear in the `restored/` folder.

---

## 🧪 Testing

### Test Backup API

Using PowerShell:

```powershell
curl.exe -X POST http://127.0.0.1:5000/backup
```

### Test Backup History

```text
http://127.0.0.1:5000/backups
```

### Test Home Page

```text
http://127.0.0.1:5000/
```

---

## 📊 Example Workflow

```text
        LOCAL COMPUTER
             │
             ▼
       ┌─────────────┐
       │  files/     │
       │  test.txt   │
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │ ZIP Backup  │
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │   Boto3     │
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │  Amazon S3  │
       └──────┬──────┘
              │
              │ Restore
              ▼
       ┌─────────────┐
       │  restored/  │
       └─────────────┘
```

---

## 🔒 Security Considerations

* The S3 bucket should remain private.
* AWS credentials should never be hard-coded in Python files.
* AWS credentials should not be uploaded to GitHub.
* `.env` or credential files should be added to `.gitignore`.
* Only required AWS permissions should be granted.

Example `.gitignore`:

```text
__pycache__/
*.pyc
.env
.venv/
venv/
backups/*.zip
```

---

## 💰 Cost Considerations

This project is designed for learning using AWS Free Tier resources where applicable.

To reduce unnecessary S3 usage:

* Backups are compressed using ZIP.
* Only required test files should be backed up.
* Avoid running the scheduler unnecessarily.
* Monitor AWS usage and billing.
* Delete old test backups when they are no longer needed.

---

## 🚀 Future Improvements

Possible future improvements include:

* User authentication
* Backup metadata database
* Searchable backup history
* Backup deletion from the dashboard
* File upload through the web interface
* Backup retention policies
* Encryption
* CloudWatch monitoring
* Email notifications
* Multiple S3 buckets
* Backup version management
* Secure ZIP extraction
