import React, { useState } from 'react';
import axios from 'axios';
import { useEffect } from 'react';
import "./App.css";


function VideoUpload() {
    const [outputPath, setOutputPath] = useState('');
    const [file, setFile] = useState(null);
    const [uploadedVideoPath, setUploadedVideoPath] = useState('');

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };
 
    const handleUpload = async () => {
        const formData = new FormData();

        if (file) {
            formData.append('video', file);
        }
        try {
            const response = await axios.post(
                'http://localhost:8000/upload_video/',
                formData,
                { headers: { 'Content-Type': 'multipart/form-data' } }
            );
            console.log(response.data);
            // Assuming the response includes the path or identifier of the uploaded video
            setUploadedVideoPath(response.data.file_path); // Make sure this matches the actual response
        } catch (error) {
            console.error('Error uploading video:', error);
        }
    };

    // Effect to process the video after it's uploaded
    useEffect(() => {
        if (uploadedVideoPath) {
            // Call the process_video endpoint with the file path of the uploaded video
            axios.get('http://localhost:8000/process_video', {
                params: { video_path: uploadedVideoPath }
            })
            .then(response => {
                const output = response.data.output_path;
                // Use the output path to display the video/image
                setOutputPath(output);
            })
            .catch(error => console.error('Error processing video:', error));
        }
    }, [uploadedVideoPath]); // This effect depends on the uploadedVideoPath state
 
    return (
        <div>
            <input className="fileupload" type="file" accept="video/*" onChange={handleFileChange} />
            <button className="uploadButton" onClick={handleUpload}>Upload Video</button>
            {/* Conditionally render the output based on outputPath */}
            {outputPath && <video src={outputPath} controls />}
        </div>
    );
}

export default VideoUpload;
