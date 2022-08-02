import React, { useEffect } from 'react';
import { motion, useAnimation } from 'framer-motion'
import { useInView } from 'react-intersection-observer';
import './TrackCard.css';
interface Recommendations {
  trackID: number;
  albumCover: string;
  trackName: string;
  artist: string;
  url: string;
}
interface TrackCard {
    darkMode: boolean;
    track: Recommendations;
}

export default function TrackCard(props:TrackCard) {
    const { track, darkMode } = props
    const { trackID, albumCover, trackName, artist, url } = track
    const controls = useAnimation();
    const { ref, inView } = useInView();
    useEffect(() => {
        if (inView) {
            controls.start("visible")
        }
    }, [controls, inView])
    const mainVariants = {
        hidden: {
            opacity: 0,
        },
        visible: {
            opacity: 1,
            transition: {
                ease: "easeInOut",
                duration: 1
            }
        }
    }
    const linkVariants = {
        hover: {
            scale: 1.05,
            opacity: 0.8,
            color: "#1DB954",
            x: 6,
            transition: {
                duration: 0.5,
                ease: "easeOut"
            }
        },
        tap: {
            scale: 0.9,
        }
    }

    return (
        <motion.div className="card-container" 
        key={trackID}
        initial="hidden"
        animate={controls}
        ref={ref}
        variants={mainVariants}>
            <motion.div className="card-album-container">
                <motion.img className="card-album-cover" src={albumCover}></motion.img>
            </motion.div>
            <motion.div className="card-info-container">
                <motion.p className="card-name card-text">{trackName}</motion.p>
                <motion.p className="card-artist card-text">{artist}</motion.p>
                <motion.a className="card-link card-text" 
                    href={url} 
                    target="_blank"
                    whileHover="hover"
                    whileTap="tap"
                    variants={linkVariants}>
                        Spotify Link
                </motion.a>
            </motion.div>
        </motion.div>
    )
}