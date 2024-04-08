import React, { useState, useEffect } from 'react';
import axios from 'axios';
import "./VideoUpload.css";

function VideoUpload() {
    const [outputPath, setOutputPath] = useState('');
    const [file, setFile] = useState(null);
    const [uploadedVideoPath, setUploadedVideoPath] = useState('');
    const [isUploadSuccessful, setIsUploadSuccessful] = useState(false);
    const [errorMessage, setErrorMessage] = useState(''); // State to store the error message

    const handleFileChange = (e) => {
        // Reset error message and upload status on file change
        setErrorMessage('');
        setIsUploadSuccessful(false);

        if (e.target.files.length > 0) {
            setFile(e.target.files[0]);
        } else {
            setFile(null);
        }
    };

    const handleUpload = async () => {
        // Check if a file has been selected
        if (!file) {
            setErrorMessage('Please select a file to upload.');
            return; // Exit the function if no file is selected
        }

        const formData = new FormData();
        formData.append('video', file);

        try {
            const response = await axios.post('http://localhost:8000/upload_video/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    console.log(`${percentCompleted}%`);
                }
            });
            console.log('Uploaded:', response.data);
            setIsUploadSuccessful(true);
            setErrorMessage(''); // Reset error message on successful upload
        } catch (error) {
            console.error('Error uploading video:', error);
            setErrorMessage('Error uploading video. Please try again.');
        }
    };


    const handleRemoveFile = () => {
        setFile(null);
        setIsUploadSuccessful(false);
        setErrorMessage(''); // Reset error message
    };

    return (
        <div className="file-upload-container"> 
            <h1>BiomechAnalysis</h1>
            {errorMessage && <div className="error-message">{errorMessage}</div>}
            <label className="file-upload-label">
                {isUploadSuccessful ? "Successfully Uploaded!" : (file ? file.name : "Choose a file")}
                <input type="file" onChange={handleFileChange} style={{ display: 'none' }} />
            </label>
            {file && !isUploadSuccessful && (
                <button onClick={handleRemoveFile} className="remove-file-button">Remove file</button>
            )}
            <button className="fileUpload" onClick={handleUpload} disabled={isUploadSuccessful || !file}>Upload Video</button>
            {outputPath && <video src={outputPath} controls />}
        </div>
    );
}

export default VideoUpload;
