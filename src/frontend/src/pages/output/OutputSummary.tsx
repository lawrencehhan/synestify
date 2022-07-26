import React, { useEffect } from 'react';
import { motion } from 'framer-motion'
import Circle from '../../components/Circle';
import Disk from '../../components/Disk';
interface Output {
    darkMode: boolean;
}

export default function OutputSummary(props:Output) {
    const { darkMode } = props

    return (
        <div className="summary-content">
            Placeholder for summary content
        </div>
    )
}