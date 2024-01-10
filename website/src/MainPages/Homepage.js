import React from 'react';
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
    </div>
  );
}

export default Homepage;