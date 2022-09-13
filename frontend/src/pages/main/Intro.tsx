import React from 'react';
import { motion } from 'framer-motion';
import CircleCustom from '../../components/CircleCustom';
interface Intro {
    darkMode: boolean;
}

export default function Intro(props:Intro) {
    const { darkMode } = props
    const parentVariants = {
        hidden: {
            opacity: 0,
        },
        visible: {
            opacity: 1,
            transition: {
                ease: "easeInOut",
                staggerChildren: 1.2,
            }
        },
        hide: {
            opacity: 0,
            x: -100,
            transition: {
                ease: "easeInOut",
                duration: 0.75,
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
                duration: 1.2,
            }
        },
    }
    const bubbleVariants = { 
        hidden: {
            opacity: 0,
        },
        visible: {
            opacity: 1,
            transition: {
                ease: 'easeInOut',
                duration: 1.2,
            },
        }
    }
    const textHighlight = {
        hidden: { y: 50, opacity: 0, rotate: 0},
        visible: {
            y: 0,
            opacity: 1,
            rotate: -3,
            transition: {
                ease: "easeOut",
                duration: 1.5,
            } 
        }
    };

    return (
        <motion.div className="col intro"
            key="intro"
            initial="hidden"
            animate="visible"
            exit="hide"
            variants={parentVariants}>
            <motion.div className="intro-bubbles"
                variants={bubbleVariants}>
                <CircleCustom 
                    className="intro-title-bub"
                    animated={true} 
                    xpos={0} 
                    ypos={5} 
                    radius={52}
                    time={15} 
                    initialColor={`${darkMode?'#FCECC9':'#293241'}`}
                    endColor="#B5D5FE"
                    darkMode={darkMode} />
                <CircleCustom 
                    className="intro-title-bub-large"
                    animated={true} 
                    xpos={0} 
                    ypos={10} 
                    radius={70}
                    time={10} 
                    initialColor={`${darkMode?'#FCECC9':'#293241'}`}
                    endColor="#5465FF"
                    darkMode={darkMode} />
            </motion.div>
            <motion.p className='intro-title'
                variants={childVariants}>
                <motion.span className='intro-title-text'
                variants={childVariants}>
                    what is synestify?
                </motion.span>
                <motion.span
                    className="highlightBox"
                    variants={textHighlight}>
                        &nbsp;
                </motion.span>
            </motion.p>
            <motion.p className='intro-desc'
                variants={childVariants}>
                Synestify is an image-analysis webapp that lets 
                you see the sounds of your image.&nbsp;By analyzing your
                image's tones and dynamics, synestify connects to Spotify's API
                to recommend songs that match the visual.
            </motion.p>
        </motion.div>
    )
}