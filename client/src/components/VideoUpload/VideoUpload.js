import React, { useState } from 'react';
import axios from 'axios';
import { useEffect } from 'react';
import "./VideoUpload.css";



function VideoUpload() {
    const [outputPath, setOutputPath] = useState('');
    const [file, setFile] = useState(null);
    const [uploadedVideoPath, setUploadedVideoPath] = useState('');


    const handleFileChange = (e) => {
        // Check if files are selected and update state
        if (e.target.files.length > 0) {
          setFile(e.target.files[0]);
        } else {
          setFile(null);
        }
      };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('video', file);

        try {
            const response = await axios.post('http://localhost:8000/upload_video/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    console.log(`${percentCompleted}%`);
                    // Update state here if you wish to display this in the UI
                }
            });
            console.log('Uploaded:', response.data);
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
        <div className="file-upload-container">
          <label className="file-upload-label">
            {file ? file.name : "Choose a file"}
            <input
              type="file"
              onChange={handleFileChange}
              style={{ display: 'none' }} // Hide the actual input element
            />
          </label>
          {file && <button onClick={() => setFile(null)}>Remove file</button>}
          <button className="fileUpload" onClick={handleUpload}>Upload Video</button>
     
        </div>
        );
    }
export default VideoUpload;




