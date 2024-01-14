import React from 'react';
import styles from '../styles/Header.module.css';

function Header() {
  return (
    <header className={styles.header}>
      <h1 className={styles.title}>ELEC498 Capstone</h1>
      <h2 className={styles.subtitle}>Autonomous Driver Examination System</h2>
    </header>
  );
}

export default Header;