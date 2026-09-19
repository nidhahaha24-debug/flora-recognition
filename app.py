import streamlit as st
import numpy as np
import json

from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Flora Recognition",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# PREMIUM PASTEL CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif !important;
}

html {
    scroll-behavior: smooth;
}

body {
    margin: 0;
}

.stApp {

    background:
        radial-gradient(
            circle at 5% 10%,
            rgba(255,190,215,0.48),
            transparent 25%
        ),

        radial-gradient(
            circle at 92% 8%,
            rgba(210,195,255,0.48),
            transparent 25%
        ),

        radial-gradient(
            circle at 45% 50%,
            rgba(195,240,215,0.34),
            transparent 30%
        ),

        radial-gradient(
            circle at 85% 80%,
            rgba(255,215,190,0.35),
            transparent 28%
        ),

        linear-gradient(
            135deg,
            #fff9fb 0%,
            #faf6ff 35%,
            #f4fcf7 70%,
            #fff7f3 100%
        );

    color: #403547;
    min-height: 100vh;
}

#MainMenu,
header,
footer {
    visibility: hidden;
}

.block-container {
    max-width: 1240px;
    padding-top: 1rem;
    padding-bottom: 4rem;
}

.anchor {
    scroll-margin-top: 100px;
    height: 1px;
}


/* =========================================================
   GLASS
========================================================= */

.glass {

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.82),
            rgba(255,255,255,0.52)
        );

    border:
        1px solid rgba(255,255,255,0.9);

    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);

    box-shadow:
        0 20px 55px rgba(112,83,125,0.10),
        inset 0 1px 0 rgba(255,255,255,0.95);
}


/* =========================================================
   NAVBAR
========================================================= */

.navbar {

    position: sticky;
    top: 12px;
    z-index: 999;

    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 12px 18px;

    border-radius: 25px;

    margin-bottom: 35px;
}

.brand {

    display: flex;
    align-items: center;
    gap: 11px;
}

.brand-flower {

    width: 43px;
    height: 43px;

    border-radius: 15px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 23px;

    background:
        linear-gradient(
            135deg,
            #ffd6e7,
            #e4d5ff
        );

    box-shadow:
        0 9px 22px rgba(194,125,163,0.20);

    animation:
        floating 4s ease-in-out infinite;
}

.brand-text {

    font-size: 20px;
    font-weight: 700;

    letter-spacing: -0.6px;

    color: #382c40;
}

.brand-sub {

    font-size: 8px;

    color: #a28f9f;

    letter-spacing: 1.4px;

    text-transform: uppercase;
}

.nav-links {

    display: flex;
    align-items: center;

    gap: 7px;
}

.nav-links a {

    text-decoration: none !important;

    color: #68596d !important;

    font-size: 11px !important;
    font-weight: 600 !important;

    padding: 9px 14px;

    border-radius: 999px;

    transition: all 0.25s ease;
}

.nav-links a:hover {

    background:
        rgba(255,211,230,0.55);

    color: #9b5276 !important;

    transform:
        translateY(-2px);
}

.nav-home {

    background:
        linear-gradient(
            135deg,
            #f5c8dc,
            #e9d4f7
        );

    color: #68435c !important;
}

.nav-ai {

    padding: 9px 14px;

    border-radius: 999px;

    background:
        rgba(255,255,255,0.72);

    border:
        1px solid rgba(205,160,192,0.25);

    color: #76576d;

    font-size: 10px;
    font-weight: 700;
}


/* =========================================================
   FLOATING DECOR
========================================================= */

.floating {

    position: fixed;

    pointer-events: none;

    z-index: 0;

    opacity: 0.42;

    animation:
        floating 7s ease-in-out infinite;
}

.f1 {
    left: 2%;
    top: 30%;
    font-size: 29px;
}

.f2 {
    right: 3%;
    top: 48%;
    font-size: 26px;
    animation-delay: 2s;
}

.f3 {
    left: 5%;
    bottom: 15%;
    font-size: 25px;
    animation-delay: 4s;
}

.f4 {
    right: 6%;
    bottom: 23%;
    font-size: 30px;
    animation-delay: 1s;
}

@keyframes floating {

    0%,100% {
        transform:
            translateY(0)
            rotate(0deg);
    }

    50% {
        transform:
            translateY(-17px)
            rotate(6deg);
    }
}


/* =========================================================
   HERO
========================================================= */

.hero {

    position: relative;

    min-height: 470px;

    display: flex;
    align-items: center;

    padding: 20px;

    scroll-margin-top: 100px;
}

.hero-left {

    width: 54%;

    position: relative;

    z-index: 5;
}

.hero-badge {

    display: inline-flex;

    align-items: center;

    gap: 6px;

    padding: 8px 15px;

    border-radius: 999px;

    background:
        linear-gradient(
            135deg,
            rgba(255,201,222,0.85),
            rgba(220,207,255,0.75)
        );

    color: #754c66;

    font-size: 10px;

    font-weight: 700;

    letter-spacing: 0.5px;
}

.hero h1 {

    font-size:
        clamp(48px, 6vw, 76px);

    line-height: 1;

    letter-spacing: -3px;

    margin:
        20px 0 12px;

    color: #2d2532;

    font-weight: 800;
}

.hero h1 span {

    background:
        linear-gradient(
            100deg,
            #c35d87,
            #a77bc8,
            #63a17b
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}

.hero-tagline {

    font-size: 21px;

    font-weight: 600;

    color: #544459;

    margin-bottom: 12px;
}

.hero-description {

    max-width: 555px;

    color: #7d6e80;

    font-size: 13px;

    line-height: 1.8;

    margin-bottom: 24px;
}

.scan-button {

    display: inline-flex;

    align-items: center;

    gap: 9px;

    padding: 13px 22px;

    border-radius: 999px;

    background:
        linear-gradient(
            135deg,
            #d16f9c,
            #ad7bc8
        );

    color: white !important;

    text-decoration: none !important;

    font-size: 12px;

    font-weight: 700;

    box-shadow:
        0 12px 30px
        rgba(191,103,148,0.28);

    transition: all 0.3s ease;
}

.scan-button:hover {

    transform:
        translateY(-4px)
        scale(1.02);

    box-shadow:
        0 17px 38px
        rgba(191,103,148,0.36);
}


/* =========================================================
   3D HERO
========================================================= */

.hero-visual {

    position: absolute;

    right: 1%;
    top: 20px;

    width: 48%;
    height: 420px;

    display: flex;

    justify-content: center;

    align-items: center;
}

.orb {

    width: 325px;
    height: 325px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle at 30% 25%,
            #ffffff,
            #f8d7eb 37%,
            #ddd5ff 70%,
            #c8ead7
        );

    box-shadow:
        0 35px 80px
        rgba(137,103,153,0.20),

        inset -20px -20px 50px
        rgba(169,123,180,0.14),

        inset 20px 20px 50px
        rgba(255,255,255,0.85);

    animation:
        orbFloat 6s ease-in-out infinite;
}

@keyframes orbFloat {

    0%,100% {
        transform:
            translateY(0);
    }

    50% {
        transform:
            translateY(-14px);
    }
}

.plant {

    position: absolute;

    left: 50%;
    top: 50%;

    transform:
        translate(-50%,-50%);

    font-size: 150px;

    filter:
        drop-shadow(
            0 20px 18px
            rgba(63,101,66,0.22)
        );

    animation:
        plantSway 5s ease-in-out infinite;
}

@keyframes plantSway {

    0%,100% {
        transform:
            translate(-50%,-50%)
            rotate(-3deg);
    }

    50% {
        transform:
            translate(-50%,-50%)
            rotate(4deg);
    }
}

.ai-card {

    position: absolute;

    right: 5%;
    bottom: 40px;

    padding: 12px 17px;

    border-radius: 18px;

    background:
        rgba(255,255,255,0.76);

    border:
        1px solid rgba(255,255,255,0.9);

    box-shadow:
        0 15px 35px
        rgba(111,77,125,0.14);

    backdrop-filter: blur(18px);

    color: #624b60;

    font-size: 10px;

    animation:
        floating 4s ease-in-out infinite;
}


/* =========================================================
   STATS
========================================================= */

.stats {

    display: grid;

    grid-template-columns:
        repeat(4,1fr);

    padding: 12px;

    border-radius: 25px;

    margin-bottom: 35px;
}

.stat {

    text-align: center;

    padding: 13px;

    border-right:
        1px solid
        rgba(120,95,130,0.10);
}

.stat:last-child {
    border-right: none;
}

.stat-icon {
    font-size: 19px;
}

.stat-number {

    font-size: 23px;

    font-weight: 700;

    color: #3e3044;
}

.stat-label {

    font-size: 9px;

    color: #988899;

    text-transform: uppercase;

    letter-spacing: 0.8px;
}


/* =========================================================
   SECTION
========================================================= */

.section-title {

    font-size: 28px;

    font-weight: 700;

    letter-spacing: -1px;

    color: #352a3b;

    margin-top: 38px;

    margin-bottom: 5px;
}

.section-subtitle {

    color: #8e8090;

    font-size: 11px;

    margin-bottom: 18px;
}


/* =========================================================
   SCANNER
========================================================= */

.scanner-shell {

    position: relative;

    padding: 34px;

    border-radius: 32px;

    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.88),
            rgba(255,239,247,0.72),
            rgba(242,237,255,0.72)
        );

    border:
        1px solid rgba(255,255,255,0.95);

    box-shadow:
        0 25px 65px
        rgba(113,79,128,0.12),

        inset 0 1px 0
        rgba(255,255,255,0.95);

    margin-bottom: 18px;
}

.scanner-shell:before {

    content: "";

    position: absolute;

    width: 230px;
    height: 230px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(255,190,220,0.35),
            transparent 70%
        );

    top: -100px;
    right: -60px;

    pointer-events: none;
}

.scanner-shell:after {

    content: "";

    position: absolute;

    width: 200px;
    height: 200px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(201,185,255,0.25),
            transparent 70%
        );

    bottom: -100px;
    left: -50px;

    pointer-events: none;
}

.scanner-top {

    position: relative;

    z-index: 2;

    display: flex;

    align-items: center;

    gap: 17px;

    margin-bottom: 0;
}

.scanner-icon {

    width: 58px;
    height: 58px;

    border-radius: 20px;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 27px;

    background:
        linear-gradient(
            135deg,
            #ffd8e8,
            #e6d8ff
        );

    box-shadow:
        0 12px 28px
        rgba(186,112,153,0.18);

    animation:
        scannerFloat 4s ease-in-out infinite;
}

@keyframes scannerFloat {

    0%,100% {
        transform:
            translateY(0)
            rotate(-2deg);
    }

    50% {
        transform:
            translateY(-6px)
            rotate(3deg);
    }
}

.scanner-heading {

    font-size: 21px;

    font-weight: 700;

    color: #49374d;

    margin: 0;
}

.scanner-small {

    font-size: 10px;

    color: #968798;

    margin-top: 3px;
}


/* =========================================================
   STREAMLIT FILE UPLOADER
========================================================= */

[data-testid="stFileUploader"] {

    width: 100%;

    margin-top: 12px;

    position: relative;

    z-index: 5;
}


/* Hide the normal Streamlit instructions */

[data-testid="stFileUploaderDropzoneInstructions"] {

    display: none !important;

    visibility: hidden !important;
}


/* Main dropzone */

[data-testid="stFileUploaderDropzone"] {

    min-height: 185px !important;

    width: 100% !important;

    border-radius: 26px !important;

    border:
        2px dashed
        rgba(207,116,159,0.42) !important;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.78),
            rgba(255,235,245,0.55)
        ) !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    position: relative !important;

    overflow: hidden !important;

    transition:
        all 0.3s ease !important;
}

[data-testid="stFileUploaderDropzone"]:hover {

    border-color:
        rgba(193,91,139,0.70) !important;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.92),
            rgba(250,229,243,0.78)
        ) !important;

    transform:
        translateY(-3px) !important;

    box-shadow:
        0 18px 42px
        rgba(183,105,147,0.13) !important;
}


/* =========================================================
   FIX DUPLICATE UPLOAD TEXT
========================================================= */

/*
   Streamlit's internal button contains its own text.
   We completely hide the internal text and create
   ONE clean label using ::after.
*/

[data-testid="stFileUploaderDropzone"] button {

    position: relative !important;

    width: 190px !important;

    height: 48px !important;

    min-width: 190px !important;

    min-height: 48px !important;

    padding: 0 !important;

    margin: 0 !important;

    border: none !important;

    border-radius: 999px !important;

    background:
        linear-gradient(
            135deg,
            #d478a1,
            #aa83c9
        ) !important;

    box-shadow:
        0 12px 27px
        rgba(183,105,147,0.25) !important;

    overflow: hidden !important;

    font-size: 0 !important;

    color: transparent !important;

    text-indent: -9999px !important;

    white-space: nowrap !important;

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease !important;
}


/* Hide EVERYTHING inside the button */

[data-testid="stFileUploaderDropzone"] button * {

    display: none !important;

    visibility: hidden !important;

    width: 0 !important;

    height: 0 !important;

    overflow: hidden !important;
}


/* One single visible button label */

[data-testid="stFileUploaderDropzone"] button::after {

    content:
        "🌿  Browse Leaf Image";

    display: block !important;

    position: absolute !important;

    left: 0 !important;

    top: 0 !important;

    width: 100% !important;

    height: 100% !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    color: white !important;

    font-family:
        'Poppins',
        sans-serif !important;

    font-size: 11px !important;

    font-weight: 700 !important;

    letter-spacing: 0 !important;

    text-indent: 0 !important;

    white-space: nowrap !important;
}


[data-testid="stFileUploaderDropzone"] button:hover {

    transform:
        translateY(-4px)
        scale(1.03) !important;

    box-shadow:
        0 17px 34px
        rgba(183,105,147,0.32) !important;
}


/* File size text */

[data-testid="stFileUploader"] small {

    display: block !important;

    color:
        #a18f9f !important;

    font-family:
        'Poppins',
        sans-serif !important;

    font-size:
        9px !important;

    text-align: center !important;

    margin-top: 8px !important;
}


/* Uploaded file name */

[data-testid="stFileUploaderFile"] {

    border-radius: 15px !important;

    background:
        rgba(255,255,255,0.72) !important;

    border:
        1px solid
        rgba(255,255,255,0.9) !important;
}


/* =========================================================
   IMAGE
========================================================= */

.image-card {

    padding: 9px;

    border-radius: 25px;

    background:
        rgba(255,255,255,0.64);

    border:
        1px solid rgba(255,255,255,0.9);

    box-shadow:
        0 18px 45px
        rgba(110,81,124,0.10);
}

.image-label {

    padding:
        7px 9px;

    color:
        #806e83;

    font-size:
        9px;

    text-transform:
        uppercase;

    letter-spacing:
        1px;
}


/* =========================================================
   RESULT
========================================================= */

.result-card {

    padding: 26px;

    border-radius: 27px;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.80),
            rgba(255,224,238,0.58)
        );

    border:
        1px solid
        rgba(255,255,255,0.95);

    box-shadow:
        0 22px 55px
        rgba(124,82,128,0.12);
}

.result-badge {

    display: inline-block;

    padding:
        6px 12px;

    border-radius:
        999px;

    background:
        linear-gradient(
            135deg,
            #e1f4df,
            #d8f1e9
        );

    color:
        #557b60;

    font-size:
        9px;

    font-weight:
        700;

    text-transform:
        uppercase;
}

.result-disease {

    font-size:
        29px;

    font-weight:
        700;

    color:
        #57344d;

    margin-top:
        12px;
}

.result-crop {

    color:
        #837585;

    font-size:
        12px;

    margin-top:
        4px;
}

.confidence-title {

    color:
        #917e91;

    font-size:
        9px;

    text-transform:
        uppercase;

    letter-spacing:
        0.8px;

    margin-top:
        21px;
}

.confidence-value {

    color:
        #bc5f89;

    font-size:
        25px;

    font-weight:
        700;
}

.confidence-bar {

    width:
        100%;

    height:
        8px;

    background:
        #f0e5ed;

    border-radius:
        99px;

    overflow:
        hidden;

    margin-top:
        7px;
}

.confidence-fill {

    height:
        100%;

    background:
        linear-gradient(
            90deg,
            #d47da3,
            #b58bd1
        );

    border-radius:
        99px;
}


/* =========================================================
   HEALTH
========================================================= */

.health-card {

    padding:
        24px;

    border-radius:
        27px;
}

.health-ring {

    width:
        112px;

    height:
        112px;

    border-radius:
        50%;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        conic-gradient(
            #d889aa var(--score),
            #e8e0e9 var(--score)
        );

    position:
        relative;
}

.health-ring:before {

    content:
        "";

    position:
        absolute;

    width:
        84px;

    height:
        84px;

    border-radius:
        50%;

    background:
        #fbf8fb;
}

.health-ring-number {

    position:
        relative;

    z-index:
        2;

    font-size:
        25px;

    font-weight:
        700;

    color:
        #4d3b52;
}


/* =========================================================
   CARDS
========================================================= */

.action-card,
.insight-card,
.workflow-card {

    padding:
        21px;

    border-radius:
        22px;

    height:
        100%;

    transition:
        0.3s ease;
}

.action-card:hover,
.insight-card:hover,
.workflow-card:hover {

    transform:
        translateY(-6px);

    box-shadow:
        0 18px 40px
        rgba(111,82,124,0.13);
}

.action-number {

    width:
        37px;

    height:
        37px;

    border-radius:
        13px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        linear-gradient(
            135deg,
            #efd5ff,
            #ffd9e7
        );

    color:
        #78507a;

    font-weight:
        700;

    font-size:
        11px;

    margin-bottom:
        12px;
}

.action-title,
.insight-title,
.workflow-title {

    color:
        #45354b;

    font-weight:
        700;

    font-size:
        13px;

    margin-bottom:
        6px;
}

.action-text,
.insight-text,
.workflow-text {

    color:
        #8d7e91;

    font-size:
        10px;

    line-height:
        1.7;
}

.insight-icon,
.workflow-icon {

    width:
        43px;

    height:
        43px;

    border-radius:
        14px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        linear-gradient(
            135deg,
            #e6d8ff,
            #ffd9e9
        );

    font-size:
        19px;

    margin-bottom:
        12px;
}

.workflow-card {

    text-align:
        center;
}

.workflow-icon {

    margin:
        0 auto 12px;
}


/* =========================================================
   CROP LIBRARY
========================================================= */

.crop-library {

    padding:
        21px;

    border-radius:
        25px;
}

.crop-pill {

    display:
        inline-flex;

    align-items:
        center;

    gap:
        5px;

    padding:
        9px 13px;

    margin:
        4px;

    border-radius:
        14px;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.82),
            rgba(246,225,239,0.70)
        );

    color:
        #66566b;

    font-size:
        10px;

    transition:
        0.25s ease;
}

.crop-pill:hover {

    transform:
        translateY(-4px)
        scale(1.02);

    box-shadow:
        0 10px 25px
        rgba(124,91,132,0.10);
}


/* =========================================================
   TIP
========================================================= */

.tip-card {

    padding:
        28px;

    border-radius:
        27px;

    background:
        linear-gradient(
            135deg,
            rgba(255,223,237,0.70),
            rgba(221,235,255,0.68),
            rgba(222,247,230,0.66)
        );

    border:
        1px solid
        rgba(255,255,255,0.95);

    box-shadow:
        0 20px 50px
        rgba(116,91,130,0.10);
}

.tip-title {

    font-size:
        23px;

    font-weight:
        700;

    color:
        #49364e;
}

.tip-text {

    color:
        #817487;

    font-size:
        11px;

    line-height:
        1.8;

    margin-top:
        7px;
}


/* =========================================================
   CONTACT
========================================================= */

.contact-card {

    padding:
        28px;

    border-radius:
        27px;

    text-align:
        center;
}

.contact-title {

    font-size:
        24px;

    font-weight:
        700;

    color:
        #49364e;
}

.contact-text {

    color:
        #88798b;

    font-size:
        11px;

    line-height:
        1.7;

    margin-top:
        7px;
}


/* =========================================================
   NOTICE
========================================================= */

.notice {

    margin-top:
        25px;

    padding:
        15px 18px;

    border-radius:
        18px;

    background:
        rgba(255,255,255,0.57);

    border:
        1px solid
        rgba(255,255,255,0.85);

    color:
        #8d7d90;

    font-size:
        9px;

    line-height:
        1.7;
}


/* =========================================================
   FOOTER
========================================================= */

.footer {

    text-align:
        center;

    margin-top:
        55px;

    padding-top:
        25px;

    border-top:
        1px solid
        rgba(116,91,127,0.10);

    color:
        #968898;

    font-size:
        9px;
}

.footer-name {

    font-size:
        18px;

    font-weight:
        700;

    color:
        #8d5478;
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 800px) {

    .nav-links {
        display: none;
    }

    .nav-ai {
        display: none;
    }

    .hero {

        min-height:
            690px;

        display:
            block;
    }

    .hero-left {
        width:
            100%;
    }

    .hero h1 {
        font-size:
            50px;
    }

    .hero-visual {

        width:
            100%;

        right:
            0;

        top:
            330px;

        height:
            330px;
    }

    .orb {

        width:
            260px;

        height:
            260px;
    }

    .plant {
        font-size:
            120px;
    }

    .stats {

        grid-template-columns:
            repeat(2,1fr);
    }

    .stat:nth-child(2) {
        border-right:
            none;
    }

    .scanner-shell {
        padding:
            22px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# FLOATING DECOR
# =========================================================

st.markdown("""
<div class="floating f1">🌿</div>
<div class="floating f2">🍃</div>
<div class="floating f3">🌸</div>
<div class="floating f4">🌿</div>
""", unsafe_allow_html=True)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_ai_model():

    return load_model(
        "agricare_model.keras"
    )


@st.cache_resource
def load_classes():

    with open(
        "class_names.json",
        "r"
    ) as f:

        return json.load(f)


model = load_ai_model()

class_names = load_classes()


# =========================================================
# DISEASE INFORMATION
# =========================================================

disease_info = {

    "Apple___Apple_scab": {

        "symptoms":
            "Olive or dark spots may appear on leaves and gradually become darker.",

        "prevention":
            "Maintain good airflow and remove infected plant material.",

        "management":
            "Remove affected leaves and follow locally recommended disease-management practices."
    },

    "Apple___Black_rot": {

        "symptoms":
            "Dark circular lesions and yellowing may develop on leaves.",

        "prevention":
            "Remove infected plant debris and maintain orchard hygiene.",

        "management":
            "Prune affected material and follow recommended crop protection practices."
    },

    "Apple___Cedar_apple_rust": {

        "symptoms":
            "Yellow-orange spots may appear on leaves.",

        "prevention":
            "Maintain orchard hygiene and monitor plants regularly.",

        "management":
            "Remove severely affected material and follow local recommendations."
    },

    "Tomato___Early_blight": {

        "symptoms":
            "Dark lesions with concentric ring patterns may develop on older leaves.",

        "prevention":
            "Avoid prolonged leaf wetness and maintain good plant spacing.",

        "management":
            "Remove severely affected leaves and follow locally recommended treatment."
    },

    "Tomato___Late_blight": {

        "symptoms":
            "Dark water-soaked patches can develop and spread rapidly under favorable conditions.",

        "prevention":
            "Improve air circulation and avoid unnecessary leaf wetness.",

        "management":
            "Remove severely affected material and seek local agricultural guidance."
    },

    "Tomato___healthy": {

        "symptoms":
            "The leaf appears consistent with the healthy category.",

        "prevention":
            "Continue regular monitoring, adequate nutrition and good watering practices.",

        "management":
            "No disease-specific action is indicated by this prediction."
    },

    "Potato___Early_blight": {

        "symptoms":
            "Dark spots and concentric ring patterns can appear on leaves.",

        "prevention":
            "Maintain plant spacing and avoid prolonged leaf wetness.",

        "management":
            "Remove severely affected leaves and follow local crop-management recommendations."
    },

    "Potato___Late_blight": {

        "symptoms":
            "Dark irregular patches may develop and spread quickly.",

        "prevention":
            "Maintain airflow and monitor plants during humid conditions.",

        "management":
            "Remove affected material and seek local agricultural guidance."
    },

    "Grape___Black_rot": {

        "symptoms":
            "Brown or dark leaf lesions may develop and expand.",

        "prevention":
            "Maintain canopy airflow and remove infected plant material.",

        "management":
            "Prune affected material and follow recommended disease-management practices."
    },

    "Corn_(maize)___Common_rust_": {

        "symptoms":
            "Small reddish-brown rust-colored spots may appear on leaves.",

        "prevention":
            "Monitor plants regularly and maintain good crop management.",

        "management":
            "Monitor disease progression and follow locally recommended practices."
    },

    "Squash___Powdery_mildew": {

        "symptoms":
            "White powder-like patches can develop across leaf surfaces.",

        "prevention":
            "Improve airflow and avoid overcrowding.",

        "management":
            "Remove severely affected leaves and follow local recommendations."
    }
}


# =========================================================
# PREDICTION
# =========================================================

def predict_image(image):

    image = image.convert("RGB")

    resized = image.resize(
        (224, 224)
    )

    arr = np.array(
        resized
    ).astype("float32")

    arr = preprocess_input(
        arr
    )

    arr = np.expand_dims(
        arr,
        axis=0
    )

    predictions = model.predict(
        arr,
        verbose=0
    )[0]

    top_index = int(
        np.argmax(predictions)
    )

    confidence = float(
        predictions[top_index] * 100
    )

    return (
        class_names[top_index],
        confidence
    )


# =========================================================
# HEALTH SCORE
# =========================================================

def calculate_health_score(
    disease,
    confidence
):

    if "healthy" in disease.lower():

        return (
            96,
            "Excellent plant health"
        )

    score = int(
        max(
            35,
            min(
                88,
                100 -
                (confidence * 0.55)
            )
        )
    )

    if score >= 75:

        status = "Mild attention needed"

    elif score >= 55:

        status = "Moderate attention needed"

    else:

        status = "Immediate attention recommended"

    return (
        score,
        status
    )


# =========================================================
# NAVBAR
# =========================================================

st.html("""
<div class="navbar glass">

    <div class="brand">

        <div class="brand-flower">
            🌸
        </div>

        <div>

            <div class="brand-text">
                Flora Recognition
            </div>

            <div class="brand-sub">
                AI FOR HEALTHIER PLANTS
            </div>

        </div>

    </div>

    <div class="nav-links">

        <a href="#home" class="nav-home">
            Home
        </a>

        <a href="#library">
            Library
        </a>

        <a href="#tips">
            Tips
        </a>

        <a href="#about">
            About
        </a>

        <a href="#contact">
            Contact
        </a>

    </div>

    <div class="nav-ai">
        🌿 Plant Health AI
    </div>

</div>
""")


# =========================================================
# HOME
# =========================================================

st.html("""
<div id="home" class="anchor"></div>
""")


st.html("""
<div class="hero">

    <div class="hero-left">

        <div class="hero-badge">
            ✦ AI POWERED PLANT CARE
        </div>

        <h1>
            Flora <span>Recognition</span>
        </h1>

        <div class="hero-tagline">
            Healthy plants. Brighter tomorrows.
        </div>

        <div class="hero-description">

            Upload a leaf image and let our AI identify
            the crop and recognize disease patterns from
            our trained plant-health categories.

        </div>

        <a
            href="#scanner"
            class="scan-button"
        >
            🌿 Start Scanning →
        </a>

    </div>

    <div class="hero-visual">

        <div class="orb">

            <div class="plant">
                🌿
            </div>

        </div>

        <div class="ai-card">
            ✦ AI Analysis Ready
        </div>

    </div>

</div>
""")


# =========================================================
# STATS
# =========================================================

st.html("""
<div class="stats glass">

    <div class="stat">

        <div class="stat-icon">
            🌿
        </div>

        <div class="stat-number">
            38
        </div>

        <div class="stat-label">
            AI Classes
        </div>

    </div>

    <div class="stat">

        <div class="stat-icon">
            🌸
        </div>

        <div class="stat-number">
            14
        </div>

        <div class="stat-label">
            Crop Types
        </div>

    </div>

    <div class="stat">

        <div class="stat-icon">
            🖼️
        </div>

        <div class="stat-number">
            224²
        </div>

        <div class="stat-label">
            Image Input
        </div>

    </div>

    <div class="stat">

        <div class="stat-icon">
            🧠
        </div>

        <div class="stat-number">
            AI
        </div>

        <div class="stat-label">
            MobileNetV2
        </div>

    </div>

</div>
""")


# =========================================================
# SCANNER
# =========================================================

st.html("""
<div id="scanner" class="anchor"></div>
""")


st.markdown(
    '<div class="section-title">Plant Health Scanner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Give your leaf a little check-up with Flora Recognition.</div>',
    unsafe_allow_html=True
)


st.html("""
<div class="scanner-shell">

    <div class="scanner-top">

        <div class="scanner-icon">
            🌿
        </div>

        <div>

            <div class="scanner-heading">
                Upload a Leaf Image 🌸
            </div>

            <div class="scanner-small">
                Choose a clear leaf image and let Flora AI take a look ✨
            </div>

        </div>

    </div>

</div>
""")


# =========================================================
# REAL WORKING UPLOADER
# =========================================================

uploaded_file = st.file_uploader(
    "Upload a leaf image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ],
    label_visibility="collapsed"
)


# =========================================================
# PREDICTION RESULT
# =========================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")


    left, middle, right = st.columns(
        [1.0, 1.15, 0.8],
        gap="medium"
    )


    # -----------------------------------------------------
    # IMAGE
    # -----------------------------------------------------

    with left:

        st.html("""
        <div class="image-card">

            <div class="image-label">
                🌿 Uploaded Image
            </div>

        </div>
        """)

        st.image(
            image,
            use_container_width=True
        )


    # -----------------------------------------------------
    # AI RESULT
    # -----------------------------------------------------

    with middle:

        predicted_class, confidence = predict_image(
            image
        )


        if "___" in predicted_class:

            crop, disease = predicted_class.split(
                "___",
                1
            )

        else:

            crop = "Unknown"

            disease = predicted_class


        disease_display = (
            disease
            .replace("_", " ")
            .replace("(", "")
            .replace(")", "")
        )


        st.html(f"""

        <div class="result-card">

            <div class="result-badge">
                ✦ Prediction Result
            </div>

            <div class="result-disease">
                {disease_display}
            </div>

            <div class="result-crop">

                Crop:

                <strong>
                    {crop.replace("_", " ")}
                </strong>

            </div>

            <div class="confidence-title">
                AI Confidence
            </div>

            <div class="confidence-value">
                {confidence:.2f}%
            </div>

            <div class="confidence-bar">

                <div
                    class="confidence-fill"
                    style="width:{confidence}%"
                ></div>

            </div>

        </div>

        """)


    # -----------------------------------------------------
    # HEALTH
    # -----------------------------------------------------

    with right:

        score, status = calculate_health_score(
            disease,
            confidence
        )


        st.html(f"""

        <div class="health-card glass">

            <div style="
                text-align:center;
                color:#8c7b8f;
                font-size:10px;
                text-transform:uppercase;
                letter-spacing:1px;
            ">
                Plant Health
            </div>

            <div style="
                display:flex;
                justify-content:center;
                margin:17px 0;
            ">

                <div
                    class="health-ring"
                    style="--score:{score}%"
                >

                    <div class="health-ring-number">

                        {score}

                        <span style="
                            font-size:10px;
                        ">
                            /100
                        </span>

                    </div>

                </div>

            </div>

            <div style="
                text-align:center;
                color:#806f84;
                font-size:11px;
            ">
                {status}
            </div>

        </div>

        """)


    # =====================================================
    # DISEASE INFORMATION
    # =====================================================

    info = disease_info.get(
        predicted_class,
        {
            "symptoms":
                "The model identified visual patterns associated with this category.",

            "prevention":
                "Monitor the plant regularly and maintain good crop hygiene.",

            "management":
                "Consider local agricultural guidance before applying treatment."
        }
    )


    symptoms = info["symptoms"]

    prevention = info["prevention"]

    management = info["management"]


    # =====================================================
    # INSIGHTS
    # =====================================================

    st.markdown(
        '<div class="section-title">Plant Health Insights</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">A simple interpretation of the current AI result.</div>',
        unsafe_allow_html=True
    )


    a, b, c = st.columns(
        3,
        gap="medium"
    )


    with a:

        st.html(f"""

        <div class="insight-card glass">

            <div class="insight-icon">
                🔎
            </div>

            <div class="insight-title">
                Symptoms
            </div>

            <div class="insight-text">
                {symptoms}
            </div>

        </div>

        """)


    with b:

        st.html(f"""

        <div class="insight-card glass">

            <div class="insight-icon">
                🛡️
            </div>

            <div class="insight-title">
                Prevention
            </div>

            <div class="insight-text">
                {prevention}
            </div>

        </div>

        """)


    with c:

        st.html(f"""

        <div class="insight-card glass">

            <div class="insight-icon">
                🌱
            </div>

            <div class="insight-title">
                Management
            </div>

            <div class="insight-text">
                {management}
            </div>

        </div>

        """)


    # =====================================================
    # ACTION PLAN
    # =====================================================

    st.markdown(
        '<div class="section-title">Farmer Action Plan</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Simple next steps for your plant.</div>',
        unsafe_allow_html=True
    )


    if "healthy" in disease.lower():

        actions = [

            (
                "01",
                "Inspect",
                "Continue regular visual inspection."
            ),

            (
                "02",
                "Protect",
                "Maintain balanced watering and nutrition."
            ),

            (
                "03",
                "Manage",
                "Keep the growing area clean."
            ),

            (
                "04",
                "Monitor",
                "Monitor new leaves for changes."
            )

        ]

    else:

        actions = [

            (
                "01",
                "Inspect",
                "Check nearby leaves for similar symptoms."
            ),

            (
                "02",
                "Protect",
                prevention
            ),

            (
                "03",
                "Manage",
                management
            ),

            (
                "04",
                "Monitor",
                "Keep checking the plant for new changes."
            )

        ]


    cols = st.columns(
        4,
        gap="medium"
    )


    for col, action in zip(
        cols,
        actions
    ):

        with col:

            number, title, text = action


            st.html(f"""

            <div class="action-card glass">

                <div class="action-number">
                    {number}
                </div>

                <div class="action-title">
                    {title}
                </div>

                <div class="action-text">
                    {text}
                </div>

            </div>

            """)


# =========================================================
# SUPPORTED CROP LIBRARY
# =========================================================

st.html("""
<div id="library" class="anchor"></div>
""")


st.markdown(
    '<div class="section-title">Supported Crop Library</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">14 crop types · 38 predefined crop and health categories</div>',
    unsafe_allow_html=True
)


crop_names = [

    "🍎 Apple",
    "🫐 Blueberry",
    "🍒 Cherry",
    "🌽 Corn",
    "🍇 Grape",
    "🍊 Orange",
    "🍑 Peach",
    "🌶️ Pepper",
    "🥔 Potato",
    "🫐 Raspberry",
    "🌱 Soybean",
    "🎃 Squash",
    "🍓 Strawberry",
    "🍅 Tomato"

]


crop_html = """
<div class="crop-library glass">
"""


for crop in crop_names:

    crop_html += f"""

    <span class="crop-pill">
        {crop}
    </span>

    """


crop_html += """
</div>
"""


st.html(
    crop_html
)


# =========================================================
# ABOUT / WORKFLOW
# =========================================================

st.html("""
<div id="about" class="anchor"></div>
""")


st.markdown(
    '<div class="section-title">How Flora Recognition Works</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">From a leaf photo to an AI-assisted plant health result.</div>',
    unsafe_allow_html=True
)


workflow = [

    (
        "📸",
        "01. Upload",
        "Add a clear leaf image."
    ),

    (
        "⚙️",
        "02. Process",
        "The image is resized and prepared."
    ),

    (
        "🧠",
        "03. Analyze",
        "MobileNetV2 analyzes visual patterns."
    ),

    (
        "🌿",
        "04. Insights",
        "Receive crop and disease information."
    )

]


workflow_cols = st.columns(
    4,
    gap="medium"
)


for col, item in zip(
    workflow_cols,
    workflow
):

    with col:

        icon, title, text = item


        st.html(f"""

        <div class="workflow-card glass">

            <div class="workflow-icon">
                {icon}
            </div>

            <div class="workflow-title">
                {title}
            </div>

            <div class="workflow-text">
                {text}
            </div>

        </div>

        """)


# =========================================================
# TIPS
# =========================================================

st.html("""
<div id="tips" class="anchor"></div>
""")


st.markdown(
    '<div class="section-title">Smart Farming Tips 🌸</div>',
    unsafe_allow_html=True
)


st.html("""
<div class="tip-card">

    <div class="tip-title">
        Small steps today. Healthier plants tomorrow.
    </div>

    <div class="tip-text">

        For the best AI-assisted result, photograph the leaf
        in good lighting. Keep the main leaf visible and
        avoid excessive blur, shadows or obstruction.

        <br><br>

        Regularly inspect new leaves and surrounding plants
        so that changes can be noticed early.

    </div>

</div>
""")


# =========================================================
# CONTACT
# =========================================================

st.html("""
<div id="contact" class="anchor"></div>
""")


st.markdown(
    '<div class="section-title">Contact</div>',
    unsafe_allow_html=True
)


st.html("""
<div class="contact-card glass">

    <div class="contact-title">
        🌸 Flora Recognition
    </div>

    <div class="contact-text">

        Built as an AI-powered academic project focused on
        crop leaf recognition and plant disease awareness.

        <br><br>

        Flora Recognition · AI for Healthier Plants 🌿

    </div>

</div>
""")


# =========================================================
# NOTICE
# =========================================================

st.html("""
<div class="notice">

    🌸 <strong>AI Guidance Notice:</strong>

    Flora Recognition is trained on a predefined set of
    crop and disease categories. Images substantially
    different from the training data may produce unreliable
    predictions.

    Important crop-health decisions should be verified
    with qualified agricultural guidance.

</div>
""")


# =========================================================
# FOOTER
# =========================================================

st.html("""
<div class="footer">

    <div class="footer-name">
        🌸 Flora Recognition
    </div>

    <div style="margin-top:5px;">
        AI for Healthier Plants
    </div>

    <div style="margin-top:12px;">
        Better Plants · Healthier Food · A Greener Future 🌿
    </div>

</div>
""")