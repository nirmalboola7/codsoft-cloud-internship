# Cloud Data Deduplication System

A cloud-based file deduplication system that detects duplicate files using SHA-256 hashing and stores unique files in Amazon S3.

## Features

- File upload
- SHA-256 hashing
- Duplicate file detection
- Amazon S3 storage
- Flask backend
- HTML, CSS and JavaScript frontend
- Storage usage tracking
- Duplicate files blocked
- Dashboard statistics

## Technologies Used

- Python
- Flask
- Boto3
- Amazon S3
- HTML
- CSS
- JavaScript
- SHA-256

## Project Structure

Task-2/
+-- README.md
+-- backend/
¦   +-- app.py
¦   +-- requirements.txt
+-- frontend/
    +-- index.html
    +-- script.js
    +-- style.css

## How It Works

1. User selects a file.
2. The frontend sends the file to the Flask backend.
3. The backend generates a SHA-256 hash.
4. The system checks whether the file already exists.
5. If the file is a duplicate, it is rejected.
6. If the file is unique, it is uploaded to Amazon S3.
7. Dashboard statistics are updated.

## AWS Configuration

AWS Region: Asia Pacific (Mumbai)

Region Code: ap-south-1

The application uses Amazon S3 for cloud storage.

## Running the Backend

Open PowerShell inside the backend folder:

.\venv\Scripts\python.exe app.py

The backend runs at:

http://127.0.0.1:5000

## Project Goal

The goal of this project is to reduce unnecessary cloud storage by preventing duplicate files from being stored multiple times.

## Task

Cloud Computing Project - Task 2
