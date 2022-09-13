import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion'
import Plot, { Figure } from 'react-plotly.js';
import CircleCustom from '../../components/CircleCustom';
import Disk from '../../components/Disk';
interface UserData {
    targetGenre: string;
    targetImage: File | null;
    imageInfo: {
      largeImage: boolean;
      imageSize: number;
    };
    imageUrl?: string;
    spotifyGenres?: string[];
  }
interface targetSeedData {
    seed: string;
    name: string;
}
interface Recommendations {
    trackID: number;
    albumCover: string;
    trackName: string;
    artist: string;
    url: string;
}
interface AnalysisResults {
    analyzed: boolean;
    targetGenre: string;
    targetArtist: targetSeedData;
    targetTrack: targetSeedData;
    score: {
        energy: number;
        loudness: number;
        tempo: number;
    };
    recommendations: [Recommendations];
    pieGraphJSON: Figure;
}
interface Output {
    userData: UserData;
    analysisResults: AnalysisResults;
    darkMode: boolean;
}


const imageGroupVariants = { 
    hidden: {
        opacity: 0,
    },
    visible: {
        opacity: 1,
        transition: {
            delay: 2.5,
            ease: "easeInOut",
            duration: 2
        }
    }
}
const imageVariants = {
    hidden: {
    },
    visible: {
        opacity: 1,
        y: [-8, 0, -8, 0, -8],
        transition: {
            delay: 2.5,
            repeat: Infinity,
            ease: "easeInOut",
            duration: 8,
        }
    }
}
const summaryTextVariants = {
    hidden: {
        opacity: 0,
    },
    visible: {
        opacity: 1,
        transition: {
            delay: 2.5, 
            ease: 'easeInOut',
            duration: 2,
        }
    }
}

const da = {
    "data": [{
        "customdata": [["#838386"], ["#F2F7FC"], ["#261913"], ["#6B5946"], ["#B8CEE4"]], "domain": {"x": [0.0, 1.0], "y": [0.0, 1.0]}, "hovertemplate": "Color HEX Value=%{label}<br>CENTROID_VOLUME=%{value}<br>CENTROID_COLOR_HEX=%{customdata[0]}<extra></extra>", "labels": ["#838386", "#F2F7FC", "#261913", "#6B5946", "#B8CEE4"], "legendgroup": "", "marker": {"colors": ["#838386", "#F2F7FC", "#261913", "#6B5946", "#B8CEE4"]}, "name": "", "showlegend": true, "values": [52410, 37494, 32444, 23043, 15166], "type": "pie", "textinfo": "percent+label"}], "layout": {"template": {"data": {"histogram2dcontour": [{"type": "histogram2dcontour", "colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}], "choropleth": [{"type": "choropleth", "colorbar": {"outlinewidth": 0, "ticks": ""}}], "histogram2d": [{"type": "histogram2d", "colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}], "heatmap": [{"type": "heatmap", "colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}], "heatmapgl": [{"type": "heatmapgl", "colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}], "contourcarpet": [{"type": "contourcarpet", "colorbar": {"outlinewidth": 0, "ticks": ""}}], "contour": [{"type": "contour", "colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}], "surface": [{"type": "surface", "colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}], "mesh3d": [{"type": "mesh3d", "colorbar": {"outlinewidth": 0, "ticks": ""}}], "scatter": [{"type": "scatter", "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}}], "parcoords": [{"type": "parcoords", "line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}}], "scatterpolargl": [{"type": "scatterpolargl", "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}}], "bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "scattergeo": [{"type": "scattergeo", "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}}], "scatterpolar": [{"type": "scatterpolar", "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}}], "histogram": [{"type": "histogram", "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}}], "scattergl": [{"type": "scattergl", "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}}], "scatter3d": [{"type": "scatter3d", "line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}}], "scattermapbox": [{"type": "scattermapbox", "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}}], "scatterternary": [{"type": "scatterternary", "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}}], "scattercarpet": [{"type": "scattercarpet", "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "pie": [{"automargin": true, "type": "pie"}]}, "layout": {"autotypenumbers": "strict", "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "hovermode": "closest", "hoverlabel": {"align": "left"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"bgcolor": "#E5ECF6", "angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "ternary": {"bgcolor": "#E5ECF6", "aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]]}, "xaxis": {"gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "automargin": true, "zerolinewidth": 2}, "yaxis": {"gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "automargin": true, "zerolinewidth": 2}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white", "gridwidth": 2}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white", "gridwidth": 2}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white", "gridwidth": 2}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "geo": {"bgcolor": "white", "landcolor": "#E5ECF6", "subunitcolor": "white", "showland": true, "showlakes": true, "lakecolor": "white"}, "title": {"x": 0.05}, "mapbox": {"style": "light"}}}, "legend": {"tracegroupgap": 0}, "margin": {"t": 60}, "showlegend": false, "hovermode": false, "paper_bgcolor": "#F4F1DE"}}

export default function OutputSummary(props:Output) {
    const { userData, analysisResults, darkMode } = props

    return (
        <motion.div className="summary-content-container">
            <motion.div className="summary-content-images summary-col"
                initial="hidden"
                animate="visible"
                variants={imageGroupVariants}>
                <motion.img className={`user-image ${darkMode&&"dm-user-image"}`} 
                    src={userData.imageUrl} 
                    alt="Submitted Image"
                    initial="hidden"
                    animate="visible"
                    variants={imageVariants}>
                </motion.img>
                <Disk darkColor={"#293241"} lightColor={"#FCECC9"} darkMode={darkMode} />
            </motion.div>
            <motion.div className="summary-content-main summary-col">
                <motion.div className={`summary-content-texts ${darkMode&&"summary-content-texts-dm"}`}
                    initial="hidden"
                    animate="visible"
                    variants={summaryTextVariants}>
                    <motion.p className="summary-main-title">
                        Your Submission
                    </motion.p>
                    <motion.p className="summary-detail sub">
                        <span className={`header ${darkMode&&"header-dm"}`}>Image: &nbsp;</span>{userData.targetImage?.name}
                    </motion.p>
                    <motion.p className="summary-detail sub">
                        <span className={`header ${darkMode&&"header-dm"}`}>Genre: &nbsp;</span>{userData.targetGenre}
                    </motion.p>
                    <hr className={`summary-break ${darkMode&&'summary-break-dm'}`}></hr>
                    <motion.p className="summary-main-title score-title">
                        Synestify's Image Scores
                    </motion.p>
                    <motion.p className="summary-detail score">
                        <span className={`header ${darkMode&&"header-dm"}`}>Energy:&nbsp;</span> {analysisResults.score.energy}
                    </motion.p>
                    <motion.p className="summary-detail score">
                        <span className={`header ${darkMode&&"header-dm"}`}>Loudness:&nbsp;</span> {analysisResults.score.loudness}
                    </motion.p>
                    <motion.p className="summary-detail score">
                        <span className={`header ${darkMode&&"header-dm"}`}>Tempo:&nbsp;</span> {analysisResults.score.tempo}
                    </motion.p>

                    <CircleCustom 
                        className="main-bub bub"
                        animated={true} 
                        xpos={2.5} 
                        ypos={5} 
                        radius={100}
                        time={10} 
                        initialColor={`${darkMode?'#FCECC9':'#293241'}`}
                        endColor={darkMode ? "#5465FF" : "#B5D5FE"}
                        darkMode={darkMode} />
                    <CircleCustom 
                        className="sec-bub bub"
                        animated={true} 
                        xpos={4} 
                        ypos={8} 
                        radius={70}
                        time={15} 
                        initialColor={`${darkMode?'#FCECC9':'#293241'}`}
                        endColor={darkMode ? "#5465FF" : "#B5D5FE"}
                        darkMode={darkMode} />
                </motion.div>
                {/* <motion.div className="summary-content-graph">
                    <Plot data={analysisResults.pieGraphJSON.data} layout={analysisResults.pieGraphJSON.layout}/>
                </motion.div> */}
            </motion.div>
        </motion.div>
    )
}