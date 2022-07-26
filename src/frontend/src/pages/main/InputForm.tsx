import React, { useState } from 'react';
import { motion } from 'framer-motion';
interface UserData {
    targetGenre: string;
    targetImage: File | null;
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
        },
        visible: {
            opacity: 1,
            transition: {
                delay: 3,
                duration: 1,
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
            backgroundColor: "#81B29A",
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
        <motion.div className="col form"
            key="form"
            initial="hidden"
            animate="visible"
            exit="hide"
            variants={parentVariants}>
            
            <p className='form-desc'>
                A bit more information for analysis..
            </p>
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
                    accept=".jpg, .jpeg, .png"
                    onChange={handleImageChange}
                    // accept="image/*" for any image acceptance
                >
                </input>
                <br></br>
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
            {formWarning && <div className="form-warning">Image file exceeds 1.5Mb limit.</div>}
            <div>State Check: {userData.targetGenre}</div>
        </motion.div>
    )
}