import React from 'react';
<<<<<<< HEAD
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Homepage from './MainPages/Homepage';
import Footer from './components/Footer';
import About from './MainPages/About';
import './App.css';
function App() {
  return (
    <Router>
      <div className="app-content">
        {/* Define Routes */}
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/about" element={<About />} />










        </Routes>

        <div className="App">
          {/* Other components/content */}
        </div>
      </div>
      <Footer/>
    </Router>
=======

import Homepage from './MainPages/Homepage';

function App() {
  return (
    
    <div className="App">
      
      
      <Homepage/>
    </div>
>>>>>>> 50851e3aaa4792026c789721b507ff6e2c3ff0c3
  );
}

export default App;