import React, { useState } from 'react';
import { motion } from 'framer-motion';


export default function Intro() {
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
                    className="form-dropdown-menu"
                    
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
                <button className="form-submit">Convert Visuals</button>
            </form>

        </motion.div>
    )
}