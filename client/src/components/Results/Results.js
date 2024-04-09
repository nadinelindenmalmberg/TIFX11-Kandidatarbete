import React from 'react';
import "./Results.css";
import { useLocation } from 'react-router-dom';


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
function Results() {
  const location = useLocation();
  const videoUrl = new URLSearchParams(location.search).get('videoUrl');

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
        </div>
      ) : (
        <p>No video selected</p>
      )}
    </div>
  );
}
export default Results;

