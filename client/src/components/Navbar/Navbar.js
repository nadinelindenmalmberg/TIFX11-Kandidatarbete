// src/components/Navbar/Navbar.js
import React, { useState } from 'react';
import './Navbar.css'; // Assuming you'll create a separate CSS file for the navbar

function NavBar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="navbar">
      <div className="logo">BiomechAnalysis</div>
      <button className="menu-toggle" onClick={toggleMenu}>☰</button>
      <ul className={`menu ${isOpen ? 'show' : ''}`}>
        <li><a href="#upload">Upload</a></li>
        <li><a href="#results">Results</a></li>
        <li><a href="#contact">Contact</a></li>
      </ul>
    </nav>
  );
}

export default NavBar;
