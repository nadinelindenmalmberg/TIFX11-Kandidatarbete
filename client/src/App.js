import "./App.css";
import  NavBar  from './components/Navbar/Navbar';
import VideoUpload from './components/VideoUpload/VideoUpload.js'; // Assuming VideoUpload is moved to a components folder
import Results from './components/Results/Results.js';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';


function App() {
    return (
        <Router>
            <NavBar />
            <Routes>
                <Route path="/upload" element={<VideoUpload />} />
                <Route path="/results" element={<Results />} />
                {/* Define more routes as needed */}
            </Routes>
        </Router>
    );
}

export default App;


