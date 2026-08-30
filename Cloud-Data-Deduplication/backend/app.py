from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import hashlib
import json
import os
from botocore.exceptions import ClientError
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

# AWS S3 configuration
BUCKET_NAME = "nirmal-cloud-deduplication-2026"
AWS_REGION = "ap-south-1"

# Create S3 client
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)

# Statistics file
STATS_FILE = "statistics.json"


# ---------------- STATISTICS FILE ----------------

def load_statistics():

    if not os.path.exists(STATS_FILE):

        return {
            "upload_attempts": 0,
            "duplicates_blocked": 0,
            "storage_saved": 0
        }

    with open(STATS_FILE, "r") as file:
        return json.load(file)


def save_statistics(stats):

    with open(STATS_FILE, "w") as file:
        json.dump(stats, file, indent=4)


# ---------------- HOME ----------------

@app.route("/")
def home():

    return jsonify({
        "message": "Cloud Data Deduplication System is running!"
    })


# ---------------- UPLOAD ----------------

@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:

        return jsonify({
            "error": "No file provided"
        }), 400

    file = request.files["file"]

    if file.filename == "":

        return jsonify({
            "error": "No file selected"
        }), 400

    # Read file
    file_data = file.read()

    filename = file.filename

    file_size = len(file_data)

    # Calculate SHA-256
    file_hash = hashlib.sha256(file_data).hexdigest()

    object_key = file_hash

    # Load statistics
    stats = load_statistics()

    # Count every upload attempt
    stats["upload_attempts"] += 1


    # ---------------- CHECK DUPLICATE ----------------

    try:

        s3.head_object(
            Bucket=BUCKET_NAME,
            Key=object_key
        )

        # Duplicate found
        stats["duplicates_blocked"] += 1

        # Storage that would have been used
        stats["storage_saved"] += file_size

        save_statistics(stats)

        return jsonify({

            "message": "Duplicate file detected!",

            "filename": filename,

            "size": file_size,

            "hash": file_hash,

            "duplicate": True

        })


    except ClientError as e:

        error_code = e.response["Error"]["Code"]

        if error_code not in ["404", "NoSuchKey"]:

            return jsonify({

                "error": "Error checking S3",

                "details": str(e)

            }), 500


    # ---------------- UPLOAD UNIQUE FILE ----------------

    try:

        upload_time = datetime.now(timezone.utc).isoformat()

        s3.put_object(

            Bucket=BUCKET_NAME,

            Key=object_key,

            Body=file_data,

            Metadata={

                "original-filename": filename,

                "file-size": str(file_size),

                "upload-time": upload_time

            }

        )

        save_statistics(stats)

        return jsonify({

            "message": "File uploaded successfully to S3!",

            "filename": filename,

            "size": file_size,

            "hash": file_hash,

            "duplicate": False

        })


    except ClientError as e:

        return jsonify({

            "error": "Failed to upload file",

            "details": str(e)

        }), 500


# ---------------- DASHBOARD STATISTICS ----------------

@app.route("/stats", methods=["GET"])
def statistics():

    try:

        response = s3.list_objects_v2(
            Bucket=BUCKET_NAME
        )

        objects = response.get("Contents", [])

        unique_files = len(objects)

        storage_used = sum(
            obj["Size"] for obj in objects
        )

        stats = load_statistics()

        return jsonify({

            "unique_files": unique_files,

            "storage_used": storage_used,

            "upload_attempts": stats["upload_attempts"],

            "duplicates_blocked": stats["duplicates_blocked"],

            "storage_saved": stats["storage_saved"]

        })


    except ClientError as e:

        return jsonify({

            "error": "Unable to get statistics",

            "details": str(e)

        }), 500


if __name__ == "__main__":

    app.run(debug=True)