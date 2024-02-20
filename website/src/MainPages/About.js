import React from 'react';
import styles from '../styles/about.module.css';
import Header from '../components/Header';
import Nav from '../components/Nav';
function About() {
  return (
    <div>
      {/* Header and Nav components */}
      <Header/>
      <Nav/>

      {/* Main content */}
      <div>

      <section className={styles.section}>
          <h2>Introduction</h2>
          <p>Our ELEC498 Capstone Project at Queen's University introduces an innovative Autonomous Driver Examination System, aiming to revolutionize the current driver testing methodology in Ontario. This system is designed to address the challenges faced by the existing G2 and G driver testing processes at DriveTest centres, such as scheduling difficulties, inconsistent evaluation standards, and prolonged waiting periods. By integrating advanced technology, our project endeavors to enhance the fairness, speed, and accuracy of driver examinations, ultimately contributing to safer roads in Ontario.</p>
        </section>

        <section className={styles.section}>
        <h2>Project Overview</h2>
        <p>The Autonomous Driver Examination System is a pivotal solution that targets the inefficiencies of the current driver testing framework in Ontario. With a significant increase in automobile fatalities and the need for more consistent and unbiased driver assessments, our project stands at the forefront of change. The primary objective is to develop a technology-driven system that can accurately evaluate a driver's performance in real-life scenarios, starting with the execution of a safe lane change. This system not only aims to improve the examination process but also offers a unique training tool for aspiring drivers.</p>
      </section>

      <section className={styles.section}>
        <h2>How It Works</h2>
        <p>The system operates using a blend of sophisticated hardware and software. It employs a four-camera setup to monitor the vehicle's surroundings and the driver's actions, along with an On-Board Diagnostics to track the vehicle's speed. This data is analyzed by an advanced computer vision model, which then assesses the driver's ability to safely perform a lane change. The evaluation results are then uploaded to this website, offering immediate and precise feedback. This innovative approach ensures a fair and comprehensive assessment of driving skills, surpassing the capabilities of traditional human examiners.</p>
      </section>

      <section className={styles.section}>
          <h2>Key Features</h2>
          <ul>
            <li><strong>Real-Time Monitoring:</strong> The system provides instantaneous monitoring of driving behavior, capturing every critical aspect of the driver’s performance during the test.</li>
            <li><strong>Comprehensive Skill Analysis:</strong> Utilizing advanced machine learning and computer vision, the system offers a thorough evaluation of the driver's abilities, focusing initially on the execution of a safe lane change.</li>
            <li><strong>Safety First Approach:</strong> Emphasizing safety, the system aims to cultivate a generation of more skilled and conscientious drivers, thereby contributing to the reduction of road accidents and fatalities.</li>
          </ul>
        </section>

      </div>
    </div>
  );
}
export default About;