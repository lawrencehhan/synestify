import React, { useState } from 'react';
import Intro from './components/Intro';
import InputForm from './components/InputForm';
import DarkToggle from './components/toggle/DarkToggle';
import './App.css';


export default function App() {

  // Dark Mode Handling
  const isDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const [darkMode, setDarkMode] = useState<boolean>(false)
  const handleDarkToggle = (event:React.ChangeEvent) => {
    setDarkMode( prevDarkMode => !prevDarkMode )
    event.stopPropagation()
  }


  return (
    <div className={`app ${darkMode&&"dark"}`}>
      <div className="container">
        <Intro />
        <InputForm />
      </div>
      {/* <DarkToggle darkMode={darkMode} handleDarkToggle={handleDarkToggle} /> */}
    </div>
  );
}
