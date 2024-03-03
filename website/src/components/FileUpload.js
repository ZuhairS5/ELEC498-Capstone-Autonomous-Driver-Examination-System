import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import styles from '../styles/FileUpload.module.css';

const FileUpload = ({ onValidFile }) => {
  const [file, setFile] = useState(null);

  const onDrop = useCallback(acceptedFiles => {
    const file = acceptedFiles[0];
    if (!file) {
      alert('No file selected.');
      return;
    }

    if (file.type !== 'video/mp4') {
      alert('File is not an MP4 video.');
      return;
    }

    // Attempt to check video duration
    const video = document.createElement('video');
    video.preload = 'metadata';
    
    video.onloadedmetadata = function() {
      window.URL.revokeObjectURL(video.src);
      const duration = video.duration;
      if (duration > 180) { // 180 seconds = 3 minutes
        alert('Video is longer than 3 minutes.');
        if (typeof onValidFile === 'function') {
          onValidFile(null);
        }
      } else {
        // Video is valid
        const newFile = {
          name: file.name,
          id: file.lastModified,
        };
        setFile(newFile);
        if (typeof onValidFile === 'function') {
          onValidFile(newFile);
        }
      }
    };

    video.src = URL.createObjectURL(file);
  }, [onValidFile]);

  const removeFile = (event) => {
    event.stopPropagation();
    setFile(null);
    if (typeof onValidFile === 'function') {
      onValidFile(null);
    }
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    multiple: false,
  });

  return (
    <div {...getRootProps()} className={styles.dropzone}>
      <input {...getInputProps()} />
      <p className={styles.uploadPrompt}>Click to select files</p>
      {file && (
        <div>
          <h3 className={styles.uploadedFilesTitle}>Uploaded File:</h3>
          <ul className={styles.uploadedFilesList}>
            <li key={file.id} className={styles.uploadedFileItem}>
              {file.name}
              <button onClick={removeFile} className={styles.removeButton}>X</button>
            </li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default FileUpload;