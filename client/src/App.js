import "./App.css";
import  NavBar  from './components/Navbar/Navbar';
import VideoUpload from './components/VideoUpload/VideoUpload'; // Assuming VideoUpload is moved to a components folder
import Results from './components/Results/Results'; // Make sure the path is correct
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
                <Route path="/upload" component={VideoUpload} />
                <Route path="/results" component={Results} />
                {/* Add more routes as needed */}
            </Routes> {/* Fix: Added closing tag for Routes */}
        </Router>
    );
}
export default App;



