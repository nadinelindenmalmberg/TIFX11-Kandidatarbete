// src/components/Navbar/Navbar.js
import React, { useState } from 'react';
import './Navbar.css'; // Assuming you'll create a separate CSS file for the navbar
import { Link } from 'react-router-dom'; // Import Link

function NavBar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="navbar">
      <div className="logo"></div>
      <img src="pictures/slut.png" className="coin" />
      <button className="menu-toggle" onClick={toggleMenu}>☰</button>
      <ul className={`menu ${isOpen ? 'show' : ''}`}>
        <li><Link to="/upload">Upload</Link></li>
        <li><Link to="/results">Results</Link></li>
        <li><Link to="/contact">Contact</Link></li>
      </ul>
    </nav>
  );
}

export default NavBar;
