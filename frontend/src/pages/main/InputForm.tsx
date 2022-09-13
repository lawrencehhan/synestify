import React, { useState } from 'react';
import { motion } from 'framer-motion';
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
interface Intro {
    darkMode: boolean;
    userData: UserData;
    handleFormChange: (event: React.ChangeEvent<HTMLSelectElement>) => void;
    handleImageChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    handleSubmit: (event: React.SyntheticEvent<Element, Event>) => void;
    formWarning: boolean;
    sizeWarning: boolean;
}

export default function Intro(props:Intro) {
    const { darkMode, userData, handleFormChange, handleImageChange, handleSubmit, formWarning, sizeWarning } = props

    const parentVariants = {
        hidden: {
            opacity: 0,
            rotate: 20,
            x: 400,
            y: 200,
        },
        visible: {
            opacity: 1,
            rotate: 0,
            x: 0,
            y: 0,
            transition: {
                delay: 2.5,
                duration: 1.4,
                ease: "easeInOut",
                staggerChildren: 0.5,
            }
        },
        hide: {
            opacity: 0,
            x: 100,
            transition: {
                duration: 0.75,
                ease: "easeInOut",
            }
        }
    }
    const childVariants = {
        hidden: {
            opacity: 0,
        },
        visible: {
            opacity: 1,
            transition: {
                ease: "easeInOut",
                duration: 2,
            }
        },
    }
    const buttonVariants = {
        hover: {
            scale: 1.05,
            opacity: 0.8,
            color: "#FCECC9",
            backgroundColor: "#5465FF",
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
        <motion.div className={`col form ${darkMode&&'dm-form'}`}
            key="form"
            initial="hidden"
            animate="visible"
            exit="hide"
            variants={parentVariants}>
            
            <p className='form-desc-title'>
                try it out!
            </p>
            <p className='form-desc-text'>
                enter an image you want to hear, and 
                select a genre to give the app some inspiration
            </p>
            <hr className="hr-break"></hr>
            <form onSubmit={handleSubmit} className="form-sheet">
                <label className="form-dropdown-label">Genre:&nbsp;</label>
                <select 
                    id="targetGenre"
                    value={userData.targetGenre}
                    name="targetGenre"
                    className={`form-dropdown-menu ${darkMode&&'dark'}`}
                    onChange={handleFormChange}
                >
                    <option value="">- Select a Genre -</option>
                    {userData.spotifyGenres?.map(genre => 
                        <option key={genre} value={genre}>{genre}</option>)
                    }
                </select>

                <input
                    type="file"
                    name="targetImage"
                    className="form-upload"
                    // accept=".jpg, .jpeg, .png"
                    accept="image/*"
                    onChange={handleImageChange}
                    // accept="image/*" for any image acceptance
                >
                </input>
                <hr className="form-break"></hr>
                <motion.button 
                    className="form-submit"
                    whileHover="hover"
                    whileTap="tap"
                    variants={buttonVariants}
                >
                    Convert Visuals
                </motion.button>
            </form>
            {formWarning && <div className="form-warning">Please make sure a genre and image are selected.</div>}
            {sizeWarning && <div className="form-warning">Image file exceeds 1.5Mb limit.</div>}
        </motion.div>
    )
}