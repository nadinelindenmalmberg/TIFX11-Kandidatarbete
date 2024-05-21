import React from 'react';
import "./Results.css";
import { useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';

function Results() {
  const videoUrl = localStorage.getItem('videoUrl');
  const [calculationResult, setCalculationResult] = useState();
  const [anglesData, setAnglesData] = useState([]);

  useEffect(() => {
    const filename = 'kortis.json';
    axios.get(`/calculate/${filename}`)
        .then(response => {
            if (response.data.success) {
                setAnglesData(response.data.angles || []);
                setCalculationResult(response.data.result)
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
            <div className="video-container">
                <video width="600" height="400" controls>
                    <source src={videoUrl} type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
                <h2>Angles</h2>
                {anglesData.length > 0 ? (
                    anglesData.map((fileData, index) => (
                        <div key={index} className="file-data">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Frame</th>
                                        <th>Left Knee (degrees)</th>
                                        <th>Right Knee (degrees)</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {fileData.angles && fileData.angles.length > 0 ? (
                                        fileData.angles.map((angle, idx) => (
                                            <tr key={idx}>
                                                <td>{angle.frame_id}</td>
                                                <td className="left-knee">{angle.angle1.toFixed(2)}</td>
                                                <td className="right-knee">{angle.angle2.toFixed(2)}</td>
                                            </tr>
                                        ))
                                    ) : (
                                        <tr>
                                            <td colSpan="3">No angles data available</td>
                                        </tr>
                                    )}
                                    <p>Transition: {calculationResult}</p>
                                </tbody>
                            </table>
                        </div>
                    ))
                ) : (
                    <p>Calculating...</p>
                )}
            </div>
        ) : (
            <p>No video selected</p>
        )}
    </div>
);
};

export default Results;

