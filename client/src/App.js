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
            <header className="App-header">
            <h1>BiomechAnalysis</h1>
            <VideoUpload />
            </header>
            <Routes>
                <Route path="/upload" element={<VideoUpload />} />
                <Route path="/results" element={<Results />} />
            </Routes>
        </Router>
    );
}
export default App;





