import React from 'react';
import "./Results.css";
import { useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';

function Results() {
  const location = useLocation();
  const videoUrl = localStorage.getItem('videoUrl');
  const [calculationResult, setCalculationResult] = useState();

  // ResultsPage component in your React app



    useEffect(() => {
        // Rjjjeplace 'output_123.json' with the actual file name you expect
        const filename = 'output_123.json';
        axios.get(`/calculate/${filename}`)
            .then(response => {
                if (response.data.success) {
                    setCalculationResult(response.data.result);
                } else {
                    console.error('Error fetching calculation:', response.data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }, []);


  return (
    <div className="results-container">
      <h1>Analysis Results</h1>
      {videoUrl ? (
        <div>
          <video width="320" height="240" controls>
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          {/* Add additional analysis results here if needed */}
          <h2>Calculation Result</h2>
            {calculationResult !== undefined ? (
                <p>The calculation result is: {calculationResult}</p>
            ) : (
                <p>Calculating...</p>
            )}
        </div>
      ) : (
        <p>No video selected</p>
      )}
    </div>
  );
}
export default Results;

