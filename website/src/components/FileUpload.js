import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

const FileUpload = () => {
  const onDrop = useCallback(acceptedFiles => {
    // Handle the files here
    console.log(acceptedFiles);
  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    multiple: true, // Allow multiple files
  });

  return (
    <div {...getRootProps()} style={{ border: '2px dashed #007bff', padding: '20px', textAlign: 'center' }}>
      <input {...getInputProps()} />
      <p>Drag 'n' drop some files here, or click to select files</p>
    </div>
  );
}

export default FileUpload;