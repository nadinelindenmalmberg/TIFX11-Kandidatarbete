// src/App.js

import React, { useState } from 'react';
import axios from 'axios';
//use effect
import { useEffect } from 'react';

// function VideoUpload() {
//     const [file, setFile] = useState(null);
//     const handleFileChange = (event) => {
//         setFile(event.target.files[0]);
//     };
 
//     const handleUpload = async () => {
//         const formData = new FormData();
//         if (file) {
//             formData.append('video', file);
//         }
        
//         try {
//             const response = await axios.post(
//                 'http://localhost:8000/upload_video/',
//                 formData,
//                 { headers: { 'Content-Type': 'multipart/form-data' } }
//             );
//             console.log(response.data);
//         } catch (error) {
//             console.error('Error uploading video:', error);
//         }
//     };
 
//     return (
//         <div>
//             <input type="file" accept="video/*" onChange={handleFileChange} />
//             <button onClick={handleUpload}>Upload Video</button>
//         </div>
//     );
// }
// export default VideoUpload;

 // In one of your React components

function TestBackendConnection() {
    useEffect(() => {
        // Fetch data from the Django backend
        fetch('http://localhost:8000/api/test/')
            .then(response => response.json())
            .then(data => console.log(data + "hej"));
    }, []);

    return (
        <div>
            Check the console for the backend response.
            hej
        </div>
    );
}
fetch('http://localhost:8000/api/test/')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.error('There has been a problem with your fetch operation:', error));

export default TestBackendConnection;
