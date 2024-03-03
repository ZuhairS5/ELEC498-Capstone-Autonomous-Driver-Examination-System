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

  const updateFileState = (fileCategory, fileData) => {
    setFiles(prevFiles => ({
      ...prevFiles,
      [fileCategory]: fileData,
    }));
  };

  const handleStartProcess = async () => {
    try {
      const response = await fetch(process.env.REACT_APP_BACKEND_URL, {
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
      console.log('Success:', data);
      // Handle success response, such as displaying results or next steps to the user
    } catch (error) {
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