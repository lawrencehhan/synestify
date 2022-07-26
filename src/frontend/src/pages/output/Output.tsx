import React, { useEffect } from 'react';
import { motion, useAnimation } from 'framer-motion'
import { useInView } from 'react-intersection-observer';
import './Output.css';
import OutputSummary from './OutputSummary';
import DarkToggle from './../../components/toggle/DarkToggle';
interface Output {
    darkMode: boolean;
    handleDarkToggle: (event:React.ChangeEvent)=> void;
}

export default function Output(props:Output) {
    const { darkMode, handleDarkToggle } = props
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
            }
        },
    }
    const recVariants = {
        hidden: {
            opacity: 0,
        },
        visible: {
            opacity: 1,
            transition: {
                duration: 2,
                ease: "easeInOut",
            }
        }
    }
    return (
        <motion.div className="output-container" 
        key="output"
        variants={parentVariants}>
            <div className="output-summary">
                <motion.p className='summary-title'
                initial="hidden"
                animate="visible"
                variants={summaryVariants}>
                    Synestify Summary Analysis
                </motion.p>
                <OutputSummary darkMode={darkMode} />
            </div>

            <motion.div className="output-recs"
            ref={ref}
            initial="hidden"
            animate={controls}
            variants={recVariants}>
                Curated Image-to-Songs
            </motion.div>
            <DarkToggle darkMode={darkMode} handleDarkToggle={handleDarkToggle} />
        </motion.div>
    )
}