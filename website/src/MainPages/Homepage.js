import React from 'react';
<<<<<<< HEAD
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
=======
import styles from '../styles/homepage.module.css';
import FileUpload from '../components/FileUpload';
import Footer from '../components/Footer';
function Homepage() {
  return (
    <div className={styles.App}>
      <header>
        <h1>ELEC498 Capstone</h1>
        <p>Autonomous Driver Examination System</p>
      </header>
    <FileUpload/>
      <section>
        <h2>Introduction</h2>
        <p>Welcome to the forefront of driving technology! Our ELEC498 Capstone Project...</p>
      </section>

      <section>
        <h2>Project Overview</h2>
        <p>In the era of smart vehicles and autonomous driving...</p>
      </section>

      <section>
        <h2>How It Works</h2>
        <p>Our system integrates seamlessly with specially equipped vehicles...</p>
      </section>

      <section>
        <h2>Key Features</h2>
        <ul>
          <li>Real-Time Monitoring</li>
          <li>Comprehensive Skill Analysis</li>
          <li>Safety First Approach</li>
        </ul>
      </section>
      <Footer/>
>>>>>>> 50851e3aaa4792026c789721b507ff6e2c3ff0c3
    </div>
  );
}

export default Homepage;