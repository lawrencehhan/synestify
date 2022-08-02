import React, { useEffect } from 'react';
import { motion, useAnimation } from 'framer-motion'
import { useInView } from 'react-intersection-observer';
import './Output.css';
import OutputSummary from './OutputSummary';
import TrackCard from '../../components/trackCard/TrackCard';
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
  recommendations: [Recommendations]
}
interface Output {
    darkMode: boolean;
    userData: UserData;
    analysisResults: AnalysisResults;
}

export default function Output(props:Output) {
    const { analysisResults, userData, darkMode } = props
    const controls = useAnimation();
    const { ref, inView } = useInView();
    useEffect(() => {
        if (inView) {
            controls.start("visible")
        }
    }, [controls, inView])
    const parentVariants = {
        visible: {
            transition: {
                delayChildren: 1,
            }
        }
    }
    const summaryVariants = {
        hidden: {
            opacity: 0,
        },
        visible: {
            opacity: 1,
            transition: {
                ease: "easeInOut",
                duration: 1
            }
        },
    }

    const trackCards = analysisResults.recommendations.map((rec) => {
        return (
            <TrackCard track={rec} darkMode={darkMode} />
        )
    })


    // TO-DO: 
    // - Format output images
    // - get api to send over graphjson
    // - format summary info and pop graph on with animations

    return (
        <motion.div className="output-container" 
        key="output"
        variants={parentVariants}>
            <motion.div className="output-summary">
                <motion.p className='summary-title'
                initial="hidden"
                animate="visible"
                variants={summaryVariants}>
                    Synestify Summary Analysis
                </motion.p>
                <OutputSummary darkMode={darkMode} />
                {/* <motion.img src={userData.imageUrl}></motion.img> */}
            </motion.div>
            
            {/* <motion.p className="output-cards-title">sounds title</motion.p> */}
            {trackCards}    
        </motion.div>
    )
}