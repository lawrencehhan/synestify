import React from 'react';
import { motion } from 'framer-motion';
interface Circle {
    animated: boolean;
    darkMode: boolean;
    darkColor: string;
    lightColor: string;
    xpos: number;
    ypos: number;
}

export default function Circle(props:Circle) {
    const {darkMode, animated, darkColor, lightColor, xpos, ypos} = props;
    const strokeColor = darkMode ? lightColor : darkColor;
    const strokeTransition = {
        delay: 4,
        duration: 5,
        ease: [0.6, 0.01, -0.05, 0.95]
    };
    const circleTransition = {
        delay: 4,
        repeat: Infinity,
        repeatType: undefined,
        duration: 8,
        ease: "easeInOut",
    }
    const circleVariant = {
        hidden: { x: xpos, y: ypos, },
        visible: {
            x: [xpos, xpos*1.2, xpos, xpos*0.8, xpos],
            y: [ypos, ypos*-1, ypos, ypos*-1, ypos],
            transition: circleTransition,
        }
    }

    
    return (
        <motion.svg className="svg-circle" height="300" width="300"
            viewBox="0 0 300 300"
            initial="hidden"
            animate="visible"
            variants={!animated ? undefined : circleVariant}
        >
            <motion.circle
                cx="150" 
                cy="150" 
                r="150" 
                fill="none" 
                stroke={strokeColor} 
                stroke-width="1"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={!animated ? undefined : strokeTransition}
                >
            </motion.circle>
        </motion.svg>
    )
}