import React from 'react';
import styles from '../styles/Nav.module.css';

function Nav() {
  return (
    <nav className={styles.nav}>
      <a href="/" className={styles.navButton}>
        Home
      </a>
      <a href="/about" className={styles.navButton}>
        About Us
      </a>
    </nav>
  );
}

export default Nav;