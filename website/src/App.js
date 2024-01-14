import React from 'react';
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
  );
}

export default App;