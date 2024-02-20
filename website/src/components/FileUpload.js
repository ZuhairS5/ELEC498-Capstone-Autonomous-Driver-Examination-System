import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import styles from '../styles/FileUpload.module.css';

const FileUpload = () => {
  const [file, setFile] = useState(null); // Change to hold a single file object

  const onDrop = useCallback(acceptedFiles => {
    // Since `multiple` is false, acceptedFiles[0] will always have the latest file
    const newFile = acceptedFiles[0] ? {
      name: acceptedFiles[0].name,
      id: acceptedFiles[0].lastModified
    } : null;
    setFile(newFile); // Update the state to hold the new file
  }, []);

  const removeFile = (event) => {
    event.stopPropagation();
    setFile(null); // Clear the selected file
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    multiple: false, // Ensure only one file is accepted
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
}

export default FileUpload;