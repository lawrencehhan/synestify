import React, { useState } from 'react';
import { motion } from 'framer-motion';
interface Intro {
    darkMode: boolean;
}

export default function Intro(props:Intro) {
    const { darkMode } = props
    console.log(darkMode)
    const [formData, setFormData] = React.useState(
        {
            targetGenre: "",
            targetImage: ""
        }
    )
    console.log("Target Genre: " + formData.targetGenre)

    function handleChange(event: React.ChangeEvent<HTMLSelectElement>) {
        const {name, value} = event.target
        setFormData(prevFormData => {
            return {
                ...prevFormData,
                [name]: value
            }
        })
    }
    function handleSubmit(event: React.SyntheticEvent) {
        event.preventDefault() // Preventing values from resetting on form once submitted
        // submitToApi(formData)
        console.log(formData)
    }


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
        }
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
            initial="hidden"
            animate="visible"
            variants={parentVariants}>
            
            <p className='form-desc'>
                A bit more information for analysis..
            </p>
            <form onSubmit={handleSubmit} className="form-sheet">
                <label className="form-dropdown-label">Genre:&nbsp;</label>
                <select 
                    id="targetGenre"
                    value={formData.targetGenre}
                    onChange={handleChange}
                    name="targetGenre"
                    className={`form-dropdown-menu ${darkMode&&'dark'}`}
                    
                >
                    <option value="">-- Temp --</option>
                    <option value="red">Red</option>
                    <option value="orange">Orange</option>
                    <option value="yellow">Yellow</option>
                    <option value="green">Green</option>
                    <option value="blue">Blue</option>
                    <option value="indigo">Indigo</option>
                    <option value="violet">Violet</option>
                </select>

                <input
                    type="file"
                    name="targetImage"
                    className="form-upload"
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
            <div>State Check: {formData.targetGenre}</div>
        </motion.div>
    )
}