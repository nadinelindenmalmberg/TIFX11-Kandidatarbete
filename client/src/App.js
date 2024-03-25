import "./App.css";
import  NavBar  from './components/Navbar/Navbar';
import VideoUpload from './components/VideoUpload/VideoUpload'; // Assuming VideoUpload is moved to a components folder


function App() {

    return (
      <div className="App">
        <NavBar />
        <header className="App-header">
          <h1>BiomechAnalysis</h1>
          <VideoUpload />

        </header>
        <main>
          {/* You can add more route-based components here if you're using React Router or additional components as your app grows */}
        </main>
      </div>
    );
  }
export default App;



