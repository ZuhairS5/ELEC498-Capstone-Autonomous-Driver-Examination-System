from flask import Flask, jsonify, request, send_from_directory, render_template, url_for
import requests
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import base64
from google.cloud import storage
import datetime
from google.oauth2 import service_account
import subprocess
import tempfile
import shutil
import logging

logging.info("This is an information message")

def download_ffmpeg_binary(ffmpeg_executable):
    ffmpeg_local_binary = 'ffmpeg'  # This is the name of the FFmpeg binary in the current directory
    if not os.path.isfile(ffmpeg_executable):
        shutil.copyfile(ffmpeg_local_binary, ffmpeg_executable)
        os.chmod(ffmpeg_executable, 0o755)  # Make it executable


app = Flask(__name__)

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'elec490-63e2445e079b.json'
# GCS bucket name
BUCKET_NAME = 'elec490-processing-bucket'
# Ensure the environment variable is set for the service account
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_FILE
storage_client = storage.Client()
# app = Flask(__name__, static_folder='build', static_url_path='/')

#--------------------------------------------------------------------------------------------------
#FOR PROD

# CORS(app, supports_credentials=True, origins= 'https://autonomous-driver-system.netlify.app')
# REACT_APP_FRONTEND_URL = "https://autonomous-driver-system.netlify.app/"

#FOR LOCAL
CORS(app, supports_credentials=True, origins='http://localhost:3000')
REACT_APP_FRONTEND_URL = "http://localhost:3000"
#---------------------------------------------------------------------------------------------------

# Get the absolute path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')
#-----------------------------------------------------------------------------------------------
@app.route('/api/checkPassword', methods=['POST'])
def check_password():
    try:
        user_password = request.json.get('password')
        hardcoded_password = base64.b64encode("Testing123".encode()).decode()

        if not user_password:
            return jsonify({"error": "Password is required"}), 400

        if base64.b64encode(user_password.encode()).decode() != hardcoded_password:
            return jsonify({"error": "Incorrect password"}), 403

        # Assuming the password is correct, proceed with your operation
        return jsonify({"message": "Password correct!"}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
    
#----------------------------------------------------------------------------------------
@app.route('/api/getSignedUrl', methods=['POST'])
def get_signed_url():
    content = request.json
    filename = content['filename']  # The name of the file to be uploaded
    blob_name = f'uploads/{filename}'  # Customize the path as needed

    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)

    # Generate a signed URL for uploading the file, valid for 15 minutes
    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=15),
        method="PUT",
        content_type='application/octet-stream'
    )

    return jsonify({"signedUrl": signed_url})

#----------------------------------------------------------------------------------------

def process_video(data, context):
    """Triggered by a change to a Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket_name = 'elec490-processing-bucket'  # Your bucket name
    file_name = data['name']
    logging.info(f"Function triggered by file: {file_name}")

    # Define the local and destination paths
    tmp_dir = tempfile.gettempdir()
    download_path = os.path.join(tmp_dir, os.path.basename(file_name))
    upload_session_id = file_name.split('/')[1]  # Assumes file_name includes a unique session ID
    frames_path = f"uploads/{upload_session_id}/pictures/"
    logging.info(f"Frames will be uploaded to: {frames_path}")

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(download_path)
    logging.info(f"Video downloaded to temporary storage: {download_path}")

    # Ensure FFmpeg is available
    ffmpeg_executable = os.path.join(tmp_dir, 'ffmpeg')
    download_ffmpeg_binary(ffmpeg_executable)

    # Process the video and generate frames using FFmpeg
    output_template = os.path.join(tmp_dir, "frame-%04d.png")  # Adjust the output format as needed
    try:
        subprocess.run([ffmpeg_executable, '-i', download_path, output_template], check=True)
        logging.info(f"Frames generated successfully from {download_path}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg Error: {e}")
        return

     # Upload the frames back to GCS
    for frame_file in os.listdir(tmp_dir):
        if frame_file.startswith("frame-") and frame_file.endswith(".png"):
            frame_blob = bucket.blob(f"{frames_path}{frame_file}")
            try:
                frame_blob.upload_from_filename(os.path.join(tmp_dir, frame_file))
                logging.info(f"Frame {frame_file} uploaded successfully.")
            except Exception as e:
                logging.error(f"Failed to upload frame {frame_file}: {e}")
            finally:
                # Ensure the frame file is deleted even if the upload fails
                os.remove(os.path.join(tmp_dir, frame_file))

if __name__ == '__main__':
    app.run(debug=True)