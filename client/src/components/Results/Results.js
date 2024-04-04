import React from 'react';
import "./Results.css";

// Dummy data for demonstration
const analysisResults = {
  maxForce: '500 N',
  peakStress: '120 MPa',
  flexionAngle: '60 degrees',
};


function ResultsPage() {
  return (
    <div className="results-container">
      <h1>Analysis Results</h1>
      <div className="results">
        <p><strong>Maximum Force:</strong> {analysisResults.maxForce}</p>
        <p><strong>Peak Stress:</strong> {analysisResults.peakStress}</p>
        <p><strong>Flexion Angle:</strong> {analysisResults.flexionAngle}</p>
      </div>
    </div>
  );
}

export default ResultsPage;
