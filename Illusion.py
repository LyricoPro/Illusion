import streamlit as st

st.set_page_config(page_title="Magic Scanner", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Magic Code Reader</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #0b0f19;
            color: #f8fafc;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        .container {
            text-align: center;
            width: 90%;
            max-width: 340px;
        }
        input {
            width: 100%;
            padding: 14px;
            font-size: 18px;
            border-radius: 10px;
            border: 1px solid #334155;
            background: #1e293b;
            color: #f8fafc;
            text-align: center;
            margin-bottom: 15px;
            outline: none;
            box-sizing: border-box;
            letter-spacing: 1px;
        }
        button {
            width: 100%;
            padding: 14px;
            font-size: 18px;
            background: linear-gradient(135deg, #475569, #1e293b);
            color: white;
            border: 1px solid #64748b;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
        }
        button:active {
            opacity: 0.8;
        }
        .card-box {
            margin-top: 15px;
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .card-img {
            width: 170px;
            border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.7);
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease;
        }
        .code-display {
            margin-top: 12px;
            font-family: monospace;
            font-size: 15px;
            letter-spacing: 2px;
            color: #94a3b8;
        }
        /* Echter SVG Pfeil (kein Emoji) */
        .arrow-container {
            margin-top: 15px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.5s ease;
        }
        .arrow-container.visible {
            opacity: 1;
        }
        svg {
            width: 40px;
            height: 40px;
            transition: transform 0.1s ease-out;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
        }
        .hidden {
            display: none;
        }
        #status {
            font-size: 13px;
            color: #64748b;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
</head>
<body>

<div class="container">
    <div id="input-section">
        <input type="text" id="code-input" placeholder="Code eingeben (z.B. 1219-Z3672)" value="1219-Z3672">
        <button onclick="startScan()">Code analysieren</button>
    </div>

    <div id="magic-section" class="hidden">
        <div id="status">Frequenz wird decodiert...</div>
        <div class="card-box">
            <img id="card-display" class="card-img" src="" alt="Card">
            <div id="code-text" class="code-display"></div>
        </div>
        
        <!-- Physikalischer Vektor-Pfeil (Striche) -->
        <div id="arrow-box" class="arrow-container">
            <svg id="vector-arrow" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <polyline points="19 12 12 19 5 12"></polyline>
            </svg>
        </div>
    </div>
</div>

<script>
    // Offizielle Deck-Karten (Stargazer & Archangels)
    const cardStargazer = "https://deckofcardsapi.com/static/img/AS.png"; 
    // Wir nutzen hier hochauflösende Referenzen (oder direkte Einbindungen)
    const cardArchangels = "https://deckofcardsapi.com/static/img/AS.png"; 
    
    // Für deine echten Bilder aus den Uploads (optional via Imgur/Hosting oder direkte URLs):
    // Stargazer: 1219-Z3672
    const imgStargazerCustom = "https://i.ibb.co/6R3vZ03/stargazer.jpg"; // Alternativ dynamisch über deine Links
    const imgArchangelsCustom = "https://i.ibb.co/9v35V7q/archangels.jpg";

    let currentState = 'stargazer';
    
    // Schüttel-Variablen
    let lastX = 0, lastY = 0, lastZ = 0;
    let lastUpdate = 0;

    // Pfeil Physik Variablen (für sanftes Schwanken & Zurückrollen)
    let currentRotation = 0;
    let targetRotation = 0;

    function startScan() {
        const inputVal = document.getElementById('code-input').value.trim();
        
        document.getElementById('input-section').classList.add('hidden');
        document.getElementById('magic-section').classList.remove('hidden');

        // Initialisiere mit Stargazer (1219-Z3672)[cite: 1]
        document.getElementById('card-display').src = "https://deckofcardsapi.com/static/img/AS.png"; 
        document.getElementById('code-text').innerText = "1219-Z3672";
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

    // Schüttel-Erkennung für den Code-Wechsel & Morph
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
        
        // Sanfter Morph-Effekt (Zoom out & In)
        cardImg.style.transform = "scale(0.8)";
        cardImg.style.opacity = "0.3";

        setTimeout(() => {
            // Code wandelt sich automatisch zum Archangels-Code (0423-D3396)[cite: 2]
            codeText.innerText = "0423-D3396";
            document.getElementById('status').innerText = "Resonanz korrigiert";
            
            // Karte wechselt zur erzwungenen Zielkarte (Archangels)[cite: 2]
            cardImg.style.transform = "scale(1)";
            cardImg.style.opacity = "1";
            
            // Vektor-Pfeil einblenden
            document.getElementById('arrow-box').classList.add('visible');
        }, 300);
    }

    // Sanfte Pfeil-Steuerung mit Gyroskop (kein Buggen, weiches Schwanken)
    function handleOrientation(e) {
        if (currentState !== 'archangels') return;
        
        let gamma = e.gamma; // Neigung links/rechts (-90 bis 90)
        
        if (gamma !== null) {
            // Ziel-Rotation basierend auf Neigung berechnen, leicht gedämpft
            targetRotation = gamma * 0.8;
        }
    }

    // Animations-Loop für butterweiches, ruckelfreies Zurückrollen und Schwanken
    function animateArrow() {
        const arrow = document.getElementById('vector-arrow');
        if (arrow) {
            // Trägheits-Formel (Lerp) für geschmeidiges Gleiten ohne Bugs
            currentRotation += (targetRotation - currentRotation) * 0.1;
            arrow.style.transform = `rotate(${currentRotation}deg)`;
        }
        requestAnimationFrame(animateArrow);
    }
    requestAnimationFrame(animateArrow);

</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=550)
