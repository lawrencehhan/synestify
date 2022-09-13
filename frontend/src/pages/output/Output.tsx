import React, { useEffect, useState } from 'react';
import { motion, useAnimation } from 'framer-motion'
import { useInView } from 'react-intersection-observer';
import './Output.css';
import OutputSummary from './OutputSummary';
import TrackCard from '../../components/trackCard/TrackCard';
import { Figure } from 'react-plotly.js';
interface UserData {
    targetGenre: string;
    targetImage: File | null;
    imageInfo: {
      largeImage: boolean;
      imageSize: number;
    };
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
interface Output {
    darkMode: boolean;
    userData: UserData;
    analysisResults: AnalysisResults;
}

export default function Output(props:Output) {
    const { analysisResults, userData, darkMode } = props
    const parentVariants = {
        visible: {
            transition: {
                delay: 1,
                delayChildren: 1,
            }
        }
    }
    const titleVariants = {
        hidden: {
            opacity: 0,
            y: 100,
        },
        visible: {
            opacity: [0, 1, 1, 0],
            y: [100, 0, 0, -100],
            transition: {
                ease: "easeInOut",
                duration: 2.5,
                delay: 0.5,
                times: [0, 0.3, 0.7, 1],
            }
        },
    }
    const recTitleVariants = {
        hidden: {
            opacity: 0,
            x: -200,
        },
        visible: {
            opacity: 1,
            x: 0,
            transition: {
                delay: 3,
                duration: 2,
                ease: "easeInOut",
            }
        }
    }

    const trackCards = analysisResults.recommendations.map((rec) => {
        return (
            <TrackCard key={rec.trackID} track={rec} darkMode={darkMode} />
        )
    })

    return (
        <motion.div className="output-container" 
        key="output"
        variants={parentVariants}>
            <motion.div className="output-summary">
                <motion.p className='summary-title'
                initial="hidden"
                animate="visible"
                variants={titleVariants}>
                    so what sounds did synestify find?
                </motion.p>
                <OutputSummary userData={userData} analysisResults={analysisResults} darkMode={darkMode} />

            </motion.div>

            <motion.div className="output-recs">
                <motion.p className="output-recs-title"
                    initial="hidden"
                    animate="visible"
                    variants={recTitleVariants}>
                        Synestify Recommendations
                </motion.p>
                {trackCards}
            </motion.div>
        </motion.div>
    )
}