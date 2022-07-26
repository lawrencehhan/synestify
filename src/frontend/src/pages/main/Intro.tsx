import React from 'react';
import { motion } from 'framer-motion';


export default function Intro() {
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
                duration: 1.5,
            }
        },
    }

    return (
        <motion.div className="col intro"
            key="intro"
            initial="hidden"
            animate="visible"
            exit="hide"
            variants={parentVariants}>
            <motion.p className='intro-title'
                variants={childVariants}>
                synesthesia n.
            </motion.p>
            <motion.p className='intro-desc'
                variants={childVariants}>
                syn·es·the·sia | \ ˌsi-nəs-ˈthē-zh(ē-)ə \
            </motion.p>
            <motion.p className='intro-desc'
                variants={childVariants}>
                a concomitant sensation and especially a subjective sensation or image of a sense (as of <span className='text-color'>color</span>)
                <br></br>other than the one (as of <span className='text-sound'>sound</span>) being stimulated
            </motion.p>
            <motion.p className='intro-desc' id='synestify-desc'
                variants={childVariants}>
                synestify analyzes your visual, and presents you with its sound
            </motion.p>
        </motion.div>
    )
}