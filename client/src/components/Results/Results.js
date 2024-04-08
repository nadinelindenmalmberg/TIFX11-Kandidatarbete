import React from 'react';
import "./Results.css";
import { useState, useEffect } from 'react';
import axios from 'axios';

// Dummy data for demonstration
// const analysisResults = {
//   maxForce: '500 N',
//   peakStress: '120 MPa',
//   flexionAngle: '60 degrees',
// };


// function ResultsPage() {
//   return (
//     <div className="results-container">
//       <h1>Analysis Results</h1>
//       <div className="results">
//         <p><strong>Maximum Force:</strong> {analysisResults.maxForce}</p>
//         <p><strong>Peak Stress:</strong> {analysisResults.peakStress}</p>
//         <p><strong>Flexion Angle:</strong> {analysisResults.flexionAngle}</p>
//       </div>
//     </div>
//   );
// }

// export default ResultsPage;

function Results({ fileID }) {
  const [videoUrl, setVideoUrl] = useState('');

  useEffect(() => {
    // Function to fetch the video URL
    const fetchVideoUrl = async () => {
      try {
        // Assuming you have a Django endpoint `/api/video/<file_id>/` that returns the video URL
        const response = await axios.get(`http://localhost:8000/video/${fileID}/`);
        setVideoUrl(response.data.videoUrl); // Assuming the response contains a field `videoUrl`
      } catch (error) {
        console.error('Error fetching video URL:', error);
        // Handle error (e.g., show an error message)
      }
    };

    fetchVideoUrl();
  }, [fileID]); // Dependency array ensures this effect runs when `fileID` changes

  return (
    <div className="results-container">
      {videoUrl ? (
        // If videoUrl is not empty, render the video player
        <video src={videoUrl} controls width="640" />
      ) : (
        <p>Loading video...</p>
      )}
    </div>
  );
}

export default Results;

