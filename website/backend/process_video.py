import os
import subprocess
from google.cloud import storage

def process_video(data, context):
    """Triggered by a change to a Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket_name = 'elec490-processing-bucket'  # Your bucket name
    file_name = data['name']

    # Define the local and destination paths
    download_path = f"/tmp/{os.path.basename(file_name)}"
    upload_session_id = file_name.split('/')[1]  # Assumes file_name includes a unique session ID
    frames_path = f"uploads/{upload_session_id}/pictures/"

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(download_path)

    # Process the video and generate frames using FFmpeg
    output_template = "/tmp/frame-%04d.png"  # Adjust the output format as needed
    subprocess.run(['ffmpeg', '-i', download_path, output_template], check=True)

    # Upload the frames back to GCS
    for frame_file in os.listdir('/tmp'):
        if frame_file.startswith("frame-") and frame_file.endswith(".png"):
            frame_blob = bucket.blob(f"{frames_path}{frame_file}")
            frame_blob.upload_from_filename(f"/tmp/{frame_file}")
            os.remove(f"/tmp/{frame_file}")  # Clean up the local file

    print(f"Processed and uploaded frames for {file_name}")