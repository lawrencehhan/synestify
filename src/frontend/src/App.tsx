import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion'
import Intro from './pages/main/Intro';
import InputForm from './pages/main/InputForm';
import Loading from './pages/loading/Loading';
import Output from './pages/output/Output';
import DarkToggle from './components/toggle/DarkToggle';
import './App.css';
import { Figure } from 'react-plotly.js';
interface UserData {
  targetGenre: string;
  targetImage: File | null;
  imageUrl?: string;
  spotifyGenres?: string[];
}
interface targetSeedData {
  seed: string;
  name: string;
}
interface Recommendations {
  trackID: number;
  albumCover: string;
  trackName: string;
  artist: string;
  url: string;
}
interface AnalysisResults {
  analyzed: boolean;
  targetGenre: string;
  targetArtist: targetSeedData;
  targetTrack: targetSeedData;
  score: {
    energy: number;
    loudness: number;
    tempo: number;
  };
  recommendations: [Recommendations];
  pieGraphJSON: Figure;
}

export default function App() {
  // Flask API Comms
  const [connected, setConnected] = useState<boolean>(false)
  const [userData, setUserData] = useState<UserData>({
    targetGenre: "",
    targetImage: null,
    spotifyGenres: [],
  })
  const [genresLoaded, setGenresLoaded] = useState<boolean>(false)

  useEffect(() => {
    // Status fetching from Flask API
    fetch("/status").then(
      (response) => response.json()
      .then((json) => {
        console.log(json)
        setConnected(true)
        fetch("/genres").then(
          (response) => response.json()
          .then((json) => {
            setUserData(prevData => {
              return {...prevData, ...json}
            })
            setGenresLoaded(true)
          })
          .catch((err) => setConnected(false))
        );
    })
      .catch((err) => {
        console.log(err)
        setConnected(false)
      })
    );
  }, [])

  // Input Form Data Handling
  const [analysisResults, setAnalaysisResults] = useState<AnalysisResults>()
  const [formWarning, setFormWarning] = useState<boolean>(false)
  const [sizeWarning, setSizeWarning] = useState<boolean>(false)
  const [loading, setLoading] = useState<boolean>(false)
  const [analysisComplete, setAnalysisComplete] = useState<boolean>(false)
  function handleFormChange(event: React.ChangeEvent<HTMLSelectElement> | React.ChangeEvent<HTMLInputElement>) {
      let {name, value} = event.target
      if (value === "r-n-b") { // temporary fix to spotify api's ambiguity
        value = "r&b"
      }
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
        targetImage: imageData,
        imageUrl: URL.createObjectURL(imageData)
      }
    })
    console.log("userData updated: " + event.target.name)
  }
  function submitToApi(userData: UserData) {
    if (userData.targetImage !== null && userData.targetGenre !== "") { 
      let formData = new FormData()
      formData.append("targetGenre", userData.targetGenre)
      formData.append("targetImage", userData.targetImage, userData.targetImage?.name)
      const requestOptions = {
        method: 'POST',
        body: formData
      }
      fetch('/analysis', requestOptions)
        .then(response => response.json())
        .then(result => {
          setAnalaysisResults(prevAnalysisResults => {
            return {
              ...prevAnalysisResults,
              ...result
            }
          })
          console.log("Analysis completed.")
          setLoading(false)
          setAnalysisComplete(true)
        })
        .catch(error => {
          console.log('error', error)
          setLoading(false)
        })
    }
    return
  }
  console.log(analysisResults?.pieGraphJSON)
  function handleSubmit(event: React.SyntheticEvent<Element, Event>) {
      event.preventDefault() // Preventing values from resetting on form once submitted
      if (!userData.targetImage || userData.targetGenre === "") {
        setFormWarning(prevFormWarning => {
          return prevFormWarning ? prevFormWarning : !prevFormWarning
        })
        console.log("Form submitted with incomplete data.")
      } else {
        if (userData.targetImage.size <= 1500000) {
          console.log("Analyzing following data:" + userData)
          setLoading(true) // Unmount the form page, and mount the loading animation
          submitToApi(userData)
        } else {
          setSizeWarning(prevSizeWarning => {
            return prevSizeWarning ? prevSizeWarning : !prevSizeWarning
          })
          console.log("Image file exceeded 1.5MB")
        }
      }
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
        {!connected &&
          <Loading 
            key="disconnected_synestify" 
            message="Sorry, Synestify is currently offline" 
            darkMode={darkMode} />
        }  
        {!genresLoaded && connected &&
          <Loading 
            key="loading_synestify" 
            message="Connecting to Synestify" 
            darkMode={darkMode} />
        }        
        {!analysisComplete && !loading && genresLoaded &&
          <motion.div className="main-container" key="main">
            <Intro darkMode={darkMode} />
            <InputForm darkMode={darkMode} userData={userData} handleFormChange={handleFormChange} handleImageChange={handleImageChange} handleSubmit={handleSubmit} formWarning={formWarning} sizeWarning={sizeWarning}/>
          </motion.div>  
        }
        {!analysisComplete && loading &&
          <Loading 
            key="loading_analysis" 
            message="finding your sounds . . . " 
            darkMode={darkMode} />
        }
        {analysisComplete && !loading && analysisResults &&
          <Output key="output" analysisResults={analysisResults} userData={userData} darkMode={darkMode} ></Output>
        }
        { (!analysisComplete && !loading) ? 
          <DarkToggle key="toggle-pre" darkMode={darkMode} handleDarkToggle={handleDarkToggle} /> :
          <DarkToggle key="toggle-post" darkMode={darkMode} handleDarkToggle={handleDarkToggle} />
        }
      </AnimatePresence>
    </div>
  );
}
