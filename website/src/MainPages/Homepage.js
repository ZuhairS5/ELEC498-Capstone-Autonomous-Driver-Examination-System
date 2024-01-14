import React from 'react';
import FileUpload from '../components/FileUpload';
import Header from '../components/Header';
import Nav from '../components/Nav';
import styles from '../styles/homepage.module.css'; 
function Homepage() {
  return (
    <div>
      <Header/>
      <Nav/>
      
      <div className={styles.content}>
        <h1 className={styles.title}>Upload Your Driving Footage</h1>
        <p className={styles.description}>
          Welcome to our Autonomous Driver Examination System. Please upload your driving footage here.
          Our advanced computer vision technology will analyze your driving skills and provide valuable feedback.
        </p>
        <FileUpload/>
      </div>
    </div>
  );
}

export default Homepage;