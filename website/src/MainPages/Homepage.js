import React, { useState } from 'react';

import FileUpload from '../components/FileUpload';
import Header from '../components/Header';
import Nav from '../components/Nav';
import styles from '../styles/homepage.module.css'; 


function Homepage() {
  const [files, setFiles] = useState({
    front: null,
    leftBack: null,
    rightBack: null,
    dashboard: null,
  });
  const [password, setPassword] = useState('');
  const [feedbackMessage, setFeedbackMessage] = useState({ message: '', isError: false });


  const updateFileState = (fileCategory, fileData) => {
    setFiles(prevFiles => ({
      ...prevFiles,
      [fileCategory]: fileData,
    }));
  };
  const uploadFileToBucket = async (signedUrl, file) => {
    try {
      const uploadResponse = await fetch(signedUrl, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/octet-stream',
        },
        body: file, // The file to upload
      });
  
      if (!uploadResponse.ok) {
        throw new Error(`Failed to upload file: ${file.name}`);
      }
  
      console.log(`File uploaded successfully: ${file.name}`);
    } catch (error) {
      console.error(`Error uploading file: ${file.name}`, error);
    }
  };
  const uploadFiles = async () => {
    const fileKeys = ['front', 'leftBack', 'rightBack', 'dashboard']; // Keys for your files
  
    for (const key of fileKeys) {
      const file = files[key];
      if (!file) continue; // Skip if no file is selected
  
      try {
        // Request a signed URL from your Flask backend
        const response = await fetch('http://127.0.0.1:5000/api/getSignedUrl', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ filename: file.name }),
        });
  
        if (!response.ok) {
          throw new Error('Failed to get a signed URL');
        }
  
        const { signedUrl } = await response.json();
  
        // Upload the file using the signed URL
        await uploadFileToBucket(signedUrl, file);
      } catch (error) {
        console.error('Error in uploading files:', error);
      }
    }
  };

  const handleStartProcess = async () => {
    try {

      //process.env.REACT_APP_BACKEND_URL
      const response = await fetch('http://127.0.0.1:5000/api/checkPassword', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          password: password,
        }),
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const data = await response.json();
      alert('Success: Password is correct.');
      console.log('Success:', data);
      await uploadFiles();
      // Handle success response, such as displaying results or next steps to the user
    } catch (error) {
      alert('Error: Incorrect password or network issue.');
      console.error('Error:', error);
      // Handle errors, such as displaying a notification to the user
    }
  };

  // Check if all files are selected and password is entered
  const allFilesSelected = Object.values(files).every(file => file !== null);
  const isStartEnabled = allFilesSelected && password;

  return (
    <div>
      <Header />
      <Nav />
      
      <div className={styles.content}>
        <h1 className={styles.title}>Upload Your Driving Footage</h1>
        <p className={styles.description}>
          Welcome to our Autonomous Driver Examination System. Please upload your driving footage here.
          Our advanced computer vision technology will analyze your driving skills and provide valuable feedback.
        </p>

        <h1 className={styles.title}>Upload Your Front Camera Footage</h1>
        <FileUpload onValidFile={(file) => updateFileState('front', file)} />

        <h1 className={styles.title}>Upload Your Left Back Camera Footage</h1>
        <FileUpload onValidFile={(file) => updateFileState('leftBack', file)} />

        <h1 className={styles.title}>Upload Your Right Back Camera Footage</h1>
        <FileUpload onValidFile={(file) => updateFileState('rightBack', file)} />

        <h1 className={styles.title}>Upload Your Dashboard Camera Footage</h1>
        <FileUpload onValidFile={(file) => updateFileState('dashboard', file)} />

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter Password"
          className={styles.passwordInput}
        />

        <button
          className={styles.startButton}
          onClick={handleStartProcess}
          disabled={!isStartEnabled}
        >
          Start Process
        </button>
        
      </div>
    </div>
  );
}

export default Homepage;