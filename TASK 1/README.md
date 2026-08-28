# ☁️ CodSoft Cloud File Storage

A cloud-based file storage application developed as **Task 1 of the CodSoft Cloud Internship**.

The application allows users to upload, view, download, and delete files using a Flask backend and Amazon S3 cloud storage.

---

## 🚀 Features

* 📤 Upload files to Amazon S3
* 📋 List stored files
* 📥 Download files
* 🗑️ Delete files
* 🔒 AWS IAM-based access control
* 📁 File type validation
* 📦 Maximum file size limit of 10 MB
* 🌐 Frontend connected to Flask REST APIs
* ☁️ Cloud storage using Amazon S3

---

## 🏗️ Architecture

```text
User
 │
 ▼
Frontend
HTML + CSS + JavaScript
 │
 │ HTTP Requests
 ▼
Flask Backend
Python + Flask
 │
 ▼
Boto3
 │
 ▼
AWS IAM
 │
 ▼
Amazon S3
 │
 ▼
Cloud File Storage
```

---

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask
* Flask-CORS
* Boto3

### Cloud

* Amazon S3
* AWS IAM

### Tools

* Visual Studio Code
* Git
* GitHub

---

## 📂 Project Structure

```text
TASK 1/
│
├── README.md
├── .gitignore
│
├── BACKEND/
│   ├── app.py
│   ├── requirements.txt
│   └── .env
│
└── FRONTEND/
    ├── index.html
    ├── style.css
    ├── script.js
    └── test.html
```

> The `.env` file and `venv/` directory are excluded from GitHub for security.

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
```

### 2. Open the Task 1 directory

```bash
cd codsoft-cloud-internship/TASK 1/BACKEND
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 AWS Configuration

Create a `.env` file inside the `BACKEND` folder.

```text
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
AWS_REGION=ap-south-1
S3_BUCKET_NAME=YOUR_BUCKET_NAME
```

Replace the values with your own AWS credentials.

**Never upload `.env` to GitHub.**

---

## ▶️ Run the Backend

From the `BACKEND` directory:

```bash
python app.py
```

The Flask API will run at:

```text
http://127.0.0.1:5000
```

---

## 🌐 Run the Frontend

Open:

```text
FRONTEND/index.html
```

in a web browser.

The frontend communicates with the Flask backend running on:

```text
http://127.0.0.1:5000
```

---

## 🔗 API Endpoints

| Method | Endpoint               | Description       |
| ------ | ---------------------- | ----------------- |
| GET    | `/`                    | Check API status  |
| POST   | `/upload`              | Upload a file     |
| GET    | `/files`               | List stored files |
| GET    | `/download/<filename>` | Download a file   |
| DELETE | `/delete/<filename>`   | Delete a file     |

---

## ☁️ AWS S3

The uploaded files are stored in an Amazon S3 bucket.

The application uses:

* S3 for cloud storage
* IAM for permissions
* Boto3 for communication between Python and AWS

The S3 bucket is configured with **Block Public Access enabled**, so files are not publicly accessible.

---

## 🔒 Security

The project follows basic cloud security practices:

* AWS credentials are stored in `.env`
* `.env` is excluded using `.gitignore`
* AWS IAM is used for controlled access
* S3 Block Public Access is enabled
* File type validation is implemented
* File size is limited to 10 MB

---

## 📸 Project Demonstration

Screenshots can be added here showing:

1. Frontend interface
2. File upload
3. Files displayed
4. File download
5. File deletion
6. AWS S3 bucket
7. IAM policy

---

## 🎯 Internship

**Program:** CodSoft Cloud Internship
**Task:** Task 1 – Cloud File Storage
**Developer:** Nirmal Raj Boola
