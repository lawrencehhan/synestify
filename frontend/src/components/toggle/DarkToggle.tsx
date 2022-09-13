import React from "react";
import { motion } from "framer-motion";
import Switch, { SwitchProps } from '@mui/material/Switch';
import { styled } from '@mui/material/styles';
interface ToggleProp {
    darkMode: boolean;
    handleDarkToggle: React.ChangeEventHandler<HTMLInputElement>;
    isMobile?: boolean;
}

export default function DarkToggle(props: ToggleProp) {
    const {darkMode, handleDarkToggle} = props
    const variants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                delay: 2,
                duration: 1,
                ease: "easeInOut"
            }
        },
        hide: {
            opacity: 0,
            x: -100,
            transition: {
                duration: 2,
                ease: "easeInOut"
            }
        }
    }

    // MUI IOS-styled Toggle Switch
    const IOSSwitch = styled((props: SwitchProps) => (
        <Switch 
            focusVisibleClassName=".Mui-focusVisible" 
            disableRipple 
            checked={darkMode}
            onChange={handleDarkToggle}
            {...props} />
        ))(({ theme }) => ({
            width: 42,
            height: 26,
            padding: 0,
            '& .MuiSwitch-switchBase': {
                padding: 0,
                margin: 2,
                transitionDuration: '400ms',
                '&.Mui-checked': {
                    transform: 'translateX(16px)',
                    color: '#fff',
                    '& + .MuiSwitch-track': {
                        // backgroundColor: theme.palette.mode === 'dark' ? '#2ECA45' : '#65C466',
                        backgroundColor: '#b2abf2',
                        opacity: 1,
                        border: 0,
                    },
                    '&.Mui-disabled + .MuiSwitch-track': {
                        opacity: 0.5,
                    },
                },
                '&.Mui-focusVisible .MuiSwitch-thumb': {
                    color: '#33cf4d',
                    border: '6px solid #fff',
                },
                '&.Mui-disabled .MuiSwitch-thumb': {
                    color:
                        theme.palette.mode === 'light'
                        ? theme.palette.grey[100]
                        : theme.palette.grey[600],
                },
                '&.Mui-disabled + .MuiSwitch-track': {
                    opacity: theme.palette.mode === 'light' ? 0.7 : 0.3,
                },
            },
            '& .MuiSwitch-thumb': {
                boxSizing: 'border-box',
                width: 22,
                height: 22,
            },
            '& .MuiSwitch-track': {
                borderRadius: 26 / 2,
                backgroundColor: theme.palette.mode === 'light' ? '#E9E9EA' : '#39393D',
                opacity: 1,
                transition: theme.transitions.create(['background-color'], {
                duration: 500,
                }),
            },
    }));
    return (

        <motion.div 
            className="dm-button"
            initial="hidden"
            animate="visible"
            exit="hide'"
            variants={variants}>
                <IOSSwitch />
                <img 
                    src={require(`./${darkMode?"dm_moon.png":"dm_sun.png"}`)}
                    className="dm-image"
                    alt="Darkmode Type"
                />
                <a href="https://github.com/lawrencehhan/synestify" className="icon-wrapper" target="_blank">
                    <motion.img 
                        src={require(`../assets/${darkMode ? "githubDM.png" : "github.png"}`)}
                        className='contact-icon' 
                        alt="Github"
                        initial="hidden"
                        animate="visible"
                        variants={variants}
                    />
                </a>
        </motion.div>
    )
}