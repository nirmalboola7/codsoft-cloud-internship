
import os
from io import BytesIO

import boto3
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Create Flask application
app = Flask(__name__)

# Allow frontend to communicate with backend
CORS(app)


# AWS configuration
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


# Connect to AWS S3
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)


# Allowed file extensions
ALLOWED_EXTENSIONS = {
    "txt",
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "gif",
    "doc",
    "docx",
    "xls",
    "xlsx"
}


# Maximum file size = 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024


# --------------------------------------------------
# CHECK FILE TYPE
# --------------------------------------------------

def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


# --------------------------------------------------
# HOME ROUTE
# --------------------------------------------------

@app.route("/")
def home():

    return jsonify({
        "message": "CodSoft Cloud File Storage API is running!"
    })


# --------------------------------------------------
# UPLOAD FILE
# --------------------------------------------------

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

    if not allowed_file(file.filename):

        return jsonify({
            "error": "File type is not allowed"
        }), 400

    file.seek(0, os.SEEK_END)

    file_size = file.tell()

    file.seek(0)

    if file_size > MAX_FILE_SIZE:

        return jsonify({
            "error": "File size must be less than 10 MB"
        }), 400

    try:

        s3.upload_fileobj(
            file,
            S3_BUCKET_NAME,
            file.filename
        )

        return jsonify({

            "message": "File uploaded successfully!",

            "filename": file.filename

        }), 200

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# --------------------------------------------------
# LIST FILES
# --------------------------------------------------

@app.route("/files", methods=["GET"])
def list_files():

    try:

        response = s3.list_objects_v2(
            Bucket=S3_BUCKET_NAME
        )

        files = []

        if "Contents" in response:

            for obj in response["Contents"]:

                files.append({

                    "name": obj["Key"],

                    "size": obj["Size"]

                })

        return jsonify(files)

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# --------------------------------------------------
# DOWNLOAD FILE
# --------------------------------------------------

@app.route("/download/<path:filename>", methods=["GET"])
def download_file(filename):

    try:

        file_stream = BytesIO()

        s3.download_fileobj(
            S3_BUCKET_NAME,
            filename,
            file_stream
        )

        file_stream.seek(0)

        return send_file(

            file_stream,

            as_attachment=True,

            download_name=os.path.basename(filename)

        )

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# --------------------------------------------------
# DELETE FILE
# --------------------------------------------------

@app.route("/delete/<path:filename>", methods=["DELETE"])
def delete_file(filename):

    try:

        # Delete file from S3
        s3.delete_object(

            Bucket=S3_BUCKET_NAME,

            Key=filename

        )

        return jsonify({

            "message": "File deleted successfully!",

            "filename": filename

        }), 200

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# --------------------------------------------------
# TEST ROUTE
# --------------------------------------------------

@app.route("/test")
def test():

    return "Test route is working!"


# --------------------------------------------------
# START FLASK SERVER
# --------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)

