import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import styles from '../styles/FileUpload.module.css';

const FileUpload = () => {
  const [fileNames, setFileNames] = useState([]);

  const onDrop = useCallback(acceptedFiles => {
    const newNames = acceptedFiles.map(file => ({
      name: file.name,
      id: file.lastModified
    }));
    setFileNames(prevNames => [...prevNames, ...newNames]);
  }, []);

  const removeFile = (fileId, event) => {
    event.stopPropagation();
    setFileNames(fileNames.filter(file => file.id !== fileId));
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    multiple: true,
  });

  return (
    <div {...getRootProps()} className={styles.dropzone}>
      <input {...getInputProps()} />
      <p className={styles.uploadPrompt}>Click to select files</p>
      <div>
        {fileNames.length > 0 && <h3 className={styles.uploadedFilesTitle}>Uploaded Files:</h3>}
        <ul className={styles.uploadedFilesList}>
          {fileNames.map(file => (
            <li key={file.id} className={styles.uploadedFileItem}>
              {file.name}
              <button onClick={(event) => removeFile(file.id, event)} className={styles.removeButton}>X</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default FileUpload;