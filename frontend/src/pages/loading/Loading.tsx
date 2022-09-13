import React from 'react';
import { motion } from 'framer-motion'
import Circle from '../../components/Circle'
interface LoadingPage {
    darkMode: boolean;
    message: string;
}

export default function Loading(props:LoadingPage) {
    const { darkMode, message } = props

    const variants = {
        hidden: {
            opacity: 0,
        },
        visible: {
            opacity: 1,
            transition: {
                ease: "easeInOut",
                duration: 1.2
            }
        },
        hide: {
            opacity: 0,
            x: -100,
            transition: {
                ease: "easeInOut",
                duration: 1,
            }
        }
    }
    return (
        <motion.div className="loading-container" 
        key="loading"
        initial="hidden"
        animate="visible"
        exit="hide"
        variants={variants}>
            <Circle 
                animated={true} 
                xpos={50} 
                ypos={0} 
                radius={50} 
                initialColor={`${darkMode?'#FAF3DD':'#323031'}`}
                endColor="#B2ABF2"
                darkMode={darkMode} />
            <Circle 
                animated={true} 
                xpos={-50} 
                ypos={0} 
                radius={50}
                initialColor={`${darkMode?'#FAF3DD':'#323031'}`}
                endColor="#81B29A" 
                darkMode={darkMode} />
            <motion.div 
                className="loading-subtitle">
                    {message}
            </motion.div>
        </motion.div>
    )
}