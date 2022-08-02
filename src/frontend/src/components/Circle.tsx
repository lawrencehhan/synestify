import React from 'react';
import { motion } from 'framer-motion';
interface Circle {
    animated: boolean;
    darkMode: boolean;
    initialColor: string;
    endColor: string;
    xpos: number;
    ypos: number;
    radius: number;
}

export default function Circle(props:Circle) {
    const { animated, xpos, ypos, radius, initialColor, endColor } = props;
    const boxDim = radius*2.2
    const boxDimHalf = boxDim/2
    const strokeColor = initialColor
    const boxTransition = {
        delay: 0,
        repeat: Infinity,
        repeatType: undefined,
        duration: 10,
        ease: "easeInOut",
    }
    const boxVariant = {
        hidden: { 
            x: 0, 
            y: ypos,
        },
        visible: {
            opacity: 1,
            x: [0, xpos-(-1*xpos), 0, xpos-(-1*xpos), 0],
            y: [0, ypos-(-1*ypos), 0, ypos-(-1*ypos), 0],
            transition: boxTransition,
        }
    }
    const circleVariant = { 
        hidden: {
            stroke: initialColor,
            strokeWidth: 1,
        },
        visible: {
            stroke: [initialColor, endColor, initialColor, endColor, initialColor],
            strokeWidth: [1, 2, 1, 2, 1],
            transition: boxTransition,
        }

    }

    
    return (
        <motion.svg className="svg-circle" height={boxDim} width={boxDim}
            viewBox={`0 0 ${boxDim} ${boxDim}`}
            initial="hidden"
            animate="visible"
            variants={!animated ? undefined : boxVariant}
        >
            <motion.circle
                cx={boxDimHalf} 
                cy={boxDimHalf}
                r={radius} 
                fill="none" 
                initial="hidden"
                animate="visible"
                variants={circleVariant}
                >
            </motion.circle>
        </motion.svg>
    )
}