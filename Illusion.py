import streamlit as st

# Streamlit Konfiguration für echtes Vollbild ohne weiße/blaue Ränder
st.set_page_config(page_title="Magic App", layout="wide", initial_sidebar_state="collapsed")

html_code = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Magic Matrix</title>
    <style>
        /* Kompletter Reset für echtes Schwarz ohne Streamlit-Balken */
        html, body {
            margin: 0;
            padding: 0;
            background-color: #000000 !important;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Versteckt alle Streamlit UI Elemente, die blaue/weiße Ränder erzeugen */
        #MainMenu, header, footer { visibility: hidden; }

        .container {
            text-align: center;
            width: 85%;
            max-width: 340px;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        input {
            width: 100%;
            padding: 14px;
            font-size: 16px;
            border-radius: 10px;
            border: 1px solid #27272a;
            background: #09090b;
            color: #ffffff;
            text-align: center;
            outline: none;
            box-sizing: border-box;
            letter-spacing: 1px;
        }

        input::placeholder {
            color: #52525b;
        }

        button {
            width: 100%;
            padding: 14px;
            font-size: 16px;
            background: #18181b;
            color: white;
            border: 1px solid #3f3f46;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 500;
        }

        button:active {
            background: #27272a;
        }

        .card-box {
            margin-top: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .card-img {
            width: 160px;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.9);
            transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s ease;
        }

        .code-display {
            margin-top: 15px;
            font-family: monospace;
            font-size: 16px;
            letter-spacing: 2px;
            color: #a1a1aa;
        }

        .arrow-container {
            margin-top: 20px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.4s ease;
        }

        .arrow-container.visible {
            opacity: 1;
        }

        svg {
            width: 45px;
            height: 45px;
            filter: drop-shadow(0 2px 8px rgba(56, 189, 248, 0.4));
        }

        .hidden {
            display: none !important;
        }

        #status {
            font-size: 12px;
            color: #71717a;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
    </style>
</head>
<body>

<div class="container">
    <!-- Eingabebereiche für die mathematische Matrix -->
    <div id="input-section" class="input-group">
        <input type="text" id="code-input" placeholder="Code eingeben (z.B. 1219-Z3672)">
        <input type="text" id="pos-input" placeholder="Ungefähre Position im Deck">
        <input type="date" id="date-input">
        <button onclick="startMagic()">Matrix berechnen</button>
    </div>

    <!-- Magie & Ausgabe -->
    <div id="magic-section" class="hidden">
        <div id="status">Berechne Quanten-Resonanz...</div>
        <div class="card-box">
            <img id="card-display" class="card-img" src="" alt="Card">
            <div id="code-text" class="code-display"></div>
        </div>
        
        <div id="arrow-box" class="arrow-container">
            <svg id="vector-arrow" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <polyline points="19 12 12 19 5 12"></polyline>
            </svg>
        </div>
    </div>
</div>

<script>
    const cardStargazer = "https://deckofcardsapi.com/static/img/AS.png"; 
    const cardArchangels = "https://deckofcardsapi.com/static/img/AS.png"; 

    let currentState = 'stargazer';
    
    // Physik-Variablen für sanfte Tisch-Rotation und Zurückkehren
    let currentRotation = 0;
    let targetRotation = 0;
    
    let lastX = 0, lastY = 0, lastZ = 0;
    let lastUpdate = 0;

    function startMagic() {
        const code = document.getElementById('code-input').value.trim();
        const pos = document.getElementById('pos-input').value.trim();
        
        if(!code) {
            alert("Bitte gib einen Code ein!");
            return;
        }

        document.getElementById('input-section').classList.add('hidden');
        document.getElementById('magic-section').classList.remove('hidden');

        // Startet mit Stargazer und dem eingegebenen Code[cite: 1]
        document.getElementById('card-display').src = cardStargazer;
        document.getElementById('code-text').innerText = code;
        currentState = 'stargazer';

        initSensors();
    }

    function initSensors() {
        if (typeof DeviceMotionEvent !== 'undefined' && typeof DeviceMotionEvent.requestPermission === 'function') {
            DeviceMotionEvent.requestPermission().then(response => {
                if (response == 'granted') {
                    window.addEventListener('devicemotion', handleMotion);
                }
            }).catch(console.error);
        } else {
            window.addEventListener('devicemotion', handleMotion);
        }

        if (typeof DeviceOrientationEvent !== 'undefined' && typeof DeviceOrientationEvent.requestPermission === 'function') {
            DeviceOrientationEvent.requestPermission().then(response => {
                if (response == 'granted') {
                    window.addEventListener('deviceorientation', handleOrientation);
                }
            }).catch(console.error);
        } else {
            window.addEventListener('deviceorientation', handleOrientation);
        }
    }

    // Schüttel-Erkennung (Morphing zu Archangels & Code-Wechsel)
    function handleMotion(e) {
        let current = e.accelerationIncludingGravity;
        if (!current) return;
        
        let currentTime = new Date().getTime();
        if ((currentTime - lastUpdate) > 100) {
            let diffTime = currentTime - lastUpdate;
            lastUpdate = currentTime;
            
            let speed = Math.abs(current.x + current.y + current.z - lastX - lastY - lastZ) / diffTime * 10000;
            
            if (speed > 450 && currentState === 'stargazer') {
                triggerMorph();
            }
            lastX = current.x;
            lastY = current.y;
            lastZ = current.z;
        }
    }

    function triggerMorph() {
        currentState = 'archangels';
        const cardImg = document.getElementById('card-display');
        const codeText = document.getElementById('code-text');
        
        cardImg.style.transform = "scale(0.8)";
        cardImg.style.opacity = "0.2";

        setTimeout(() => {
            // Automatischer Wechsel zum erzwungenen Archangels-Code
            codeText.innerText = "0423-D3396";[cite: 2]
            document.getElementById('status').innerText = "Matrix synchronisiert";
            
            cardImg.src = cardArchangels;[cite: 2]
            cardImg.style.transform = "scale(1)";
            cardImg.style.opacity = "1";
            
            document.getElementById('arrow-box').classList.add('visible');
        }, 300);
    }

    // Tisch-Rotation: Reagiert aufs Drehen auf dem Tisch & kehrt butterweich zurück
    function handleOrientation(e) {
        if (currentState !==
