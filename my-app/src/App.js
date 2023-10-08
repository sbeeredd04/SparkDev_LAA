import logo from './logo.svg';
import './App.css';
import NavBar from './components/NavBar';
import PictureSlider from './components/pictureSlider';
import HOME from './Pages/HOME';
import ContributeImagePage from './Pages/ContributeImagePage';

function App() {
  return (
    <div className="App">
      <header className="App-header">
      <title> LAA </title>
        {/* <NavBar/>
        <HOME /> */}
        <ContributeImagePage />

      </header>
    </div>
  );
}

export default App;
