import axios from 'axios';

// function DisplayOutput() {
//     const [outputUrl, setOutputUrl] = useState('');

//     useEffect(() => {
//         // Replace 'your_endpoint' with the actual endpoint from which you're fetching the output URL
//         axios.get('http://localhost:8000/api/processed-file-url/')
//             .then(response => {
//                 // Assuming the response body directly contains the URL or path to the output file
//                 setOutputUrl(response.data.outputUrl);
//             })
//             .catch(error => console.error('Error fetching output URL:', error));
//     }, []);

//     return (
//         <div>
//             {outputUrl && 
//                 <img src={outputUrl} alt="Output" />}
//                 {/* If it's a video, you might use a <video> tag instead of <img> */}
//         </div>
//     );
// }

// export default DisplayOutput;
