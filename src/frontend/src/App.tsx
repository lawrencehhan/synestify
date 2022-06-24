import React, { useState, useEffect } from 'react';
import Intro from './components/Intro';
import InputForm from './components/InputForm';
import DarkToggle from './components/toggle/DarkToggle';
import './App.css';
interface FormData {
  targetGenre: string;
  targetImage: string;
  spotifyGenres?: string[];
}

export default function App() {

  // Flask API Comms
  const [data, setData] = useState<FormData>({
    targetGenre: "",
    targetImage: "",
    spotifyGenres: [],
  })

  useEffect(() => {
    
  })

  // Dark Mode Handling
  const isDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const [darkMode, setDarkMode] = useState<boolean>(isDarkMode)
  const handleDarkToggle = (event:React.ChangeEvent) => {
    setDarkMode( prevDarkMode => !prevDarkMode )
    console.log("Darkmode On: " + !darkMode)
    event.stopPropagation()
  }

  return (
    <div className={`app ${darkMode&&"dark"}`}>
      <div className="container">
        <Intro />
        <InputForm darkMode={darkMode}/>
      </div>
      <DarkToggle darkMode={darkMode} handleDarkToggle={handleDarkToggle} />
    </div>
  );
}
