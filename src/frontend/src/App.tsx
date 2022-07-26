import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion'
import Intro from './pages/main/Intro';
import InputForm from './pages/main/InputForm';
import Output from './pages/output/Output';
import DarkToggle from './components/toggle/DarkToggle';
import './App.css';
import { type } from 'os';
interface UserData {
  targetGenre: string;
  targetImage: File | null;
  spotifyGenres?: string[];
}

export default function App() {
  // Flask API Comms
  const [userData, setUserData] = useState<UserData>({
    targetGenre: "",
    targetImage: null,
    spotifyGenres: [],
  })
  console.log(userData)
  // Retreiving Spotify's available genre seeds
  useEffect(() => {
    console.log("Fetching genres from flaskAPI..")
    fetch("/genres").then(
      (response) => response.json()
      .then((json) => {
        setUserData(prevData => {
          return {...prevData, ...json}
        })
      })
    );
    console.log("userData updated: spotifyGenres")
  }, [])
  // Input Form Data Handling
  const [formWarning, setFormWarning] = useState<boolean>(false)
  const [sizeWarning, setSizeWarning] = useState<boolean>(false)
  const [analysisComplete, setAnalysisComplete] = useState<boolean>(false)
  function handleFormChange(event: React.ChangeEvent<HTMLSelectElement> | React.ChangeEvent<HTMLInputElement>) {

      const {name, value} = event.target
      setUserData(prevUserData => {
          return {
              ...prevUserData,
              [name]: value
          }
      })
      console.log("userData updated: " + event.target.name)
  }
  function handleImageChange(event: React.ChangeEvent<HTMLInputElement>) {
    if (!event.target.files) return;
    const imageData = event.target.files[0]
    setUserData(prevUserData => {
      return {
        ...prevUserData,
        targetImage: imageData
      }
    })
    const formData = new FormData()
    formData.append("imageData", imageData)
    formData.append("targetGenreNew", userData.targetGenre)
    
    console.log("userData updated: " + event.target.name)
  }
  function submitToApi(userData: UserData) {
    const formData = new FormData()

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-type': 'application/json'},
      // headers: { 'Content-type': 'multipart/form-data'},
      body: JSON.stringify(userData)
    }
    fetch('/analysis', requestOptions).then(
      (response) => response.json()
      .then((json) => {
        console.log("Data submitted to flaskAPI: ")
        console.log(json)
      })
    )
    return
  }
  function handleSubmit(event: React.SyntheticEvent<Element, Event>) {
      event.preventDefault() // Preventing values from resetting on form once submitted
      if (!userData.targetImage || userData.targetGenre == "") {
        setFormWarning(prevFormWarning => {
          return prevFormWarning ? prevFormWarning : !prevFormWarning
        })
        console.log("Form submitted with incomplete data.")
      } else {
        if (userData.targetImage.size <= 1500000) {
          console.log("Analyzing following data:" + userData)
          submitToApi(userData)
          // Initiate some loading UI? 
          // Have some state variable to update as form being done once submittoapi finishes
          // let this state variable update JSX to show output page
          setAnalysisComplete(prevAnalysisComplete => !prevAnalysisComplete)
        } else {
          setSizeWarning(prevSizeWarning => {
            return prevSizeWarning ? prevSizeWarning : !prevSizeWarning
          })
          console.log("Image file exceeded 1.5MB")
        }
      }
      // setAnalysisComplete(prevAnalysisComplete => !prevAnalysisComplete) // only for testing
  }


  // Dark Mode Handling
  const isDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const [darkMode, setDarkMode] = useState<boolean>(isDarkMode)
  const handleDarkToggle = (event:React.ChangeEvent) => {
    setDarkMode( prevDarkMode => !prevDarkMode )
    console.log("Darkmode switch: " + !darkMode)
    event.stopPropagation()
  }


  return (
    <div className={`app ${darkMode&&"dark"}`}>

      <AnimatePresence exitBeforeEnter>
        {!analysisComplete &&
          <motion.div className="main-container" key="main">
            <Intro />
            <InputForm darkMode={darkMode} userData={userData} handleFormChange={handleFormChange} handleImageChange={handleImageChange} handleSubmit={handleSubmit} formWarning={formWarning} sizeWarning={sizeWarning}/>
          </motion.div>  
        }
        {analysisComplete &&
          <Output darkMode={darkMode} handleDarkToggle={handleDarkToggle}></Output>
        }
      </AnimatePresence>


      <DarkToggle darkMode={darkMode} handleDarkToggle={handleDarkToggle} />
    </div>
  );
}
