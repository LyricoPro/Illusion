import streamlit as st

st.set_page_config(page_title="Magischer Code-Scanner", layout="centered")

# HTML, CSS und JavaScript für die Magie-App
html_code = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Magischer Scanner</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0f172a;
            color: white;
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
            max-width: 350px;
        }
        input {
            width: 100%;
            padding: 12px;
            font-size: 18px;
            border-radius: 8px;
            border: 1px solid #475569;
            background: #1e293b;
            color: white;
            text-align: center;
            margin-bottom: 15px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            font-size: 18px;
            background-color: #3b82f6;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }
        button:active {
            background-color: #2563eb;
        }
        .card-container {
            margin-top: 20px;
            perspective: 1000px;
            height: 250px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .card-img {
            width: 140px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            transition: transform 0.5s ease;
        }
        .arrow {
            font-size: 50px;
            margin-top: 15px;
            transition: transform 0.2s ease;
        }
        .hidden {
            display: none;
        }
        #status {
            font-size: 14px;
            color: #94a3b8;
            margin-top: 10px;
        }
    </style>
</head>
<body>

<div class="container">
    <div id="input-section">
        <h3>Gedanken-Code eingeben</h3>
        <input type="text" id="code-input" placeholder="z.B. 1219Z3672">
        <button onclick="startScan()">Code analysieren</button>
    </div>

    <div id="magic-section" class="hidden">
        <div id="status">Scanne Gedanken-Frequenzen...</div>
        <div class="card-container">
            <!-- Platzhalter für Kartenbilder (SVG/URLs) -->
            <img id="card-display" class="card-img" src="" alt="Karte">
            <div id="arrow-display" class="arrow hidden">⬇️</div>
        </div>
    </div>
</div>

<script>
    // Liste von falschen Karten (Beispiel-Bilder aus öffentlichem Deck)
    const wrongCards = [
        {name: "Kreuz 10", img: "https://deckofcardsapi.com/static/img/0C.png"},
        {name: "Herz König", img: "https://deckofcardsapi.com/static/img/KH.png"},
        {name: "Karo Bube", img: "https://deckofcardsapi.com/static/img/JD.png"},
        {name: "Pik 7", img: "https://deckofcardsapi.com/static/img/7S.png"}
    ];
    
    const pikAsImg = "https://deckofcardsapi.com/static/img/AS.png";
    let currentState = 'input'; // input, wrong, pik
    let lastX = 0, lastY = 0, lastZ = 0;
    let shakeThreshold = 15;
    let lastUpdate = 0;

    function startScan() {
        const code = document.getElementById('code-input').value;
        if(!code) {
            alert("Bitte gib einen Code ein!");
            return;
        }

        document.getElementById('input-section').classList.add('hidden');
        document.getElementById('magic-section').classList.remove('hidden');

        // Wähle zufällige falsche Karte
        const randomCard = wrongCards[Math.floor(Math.random() * wrongCards.length)];
        document.getElementById('card-display').src = randomCard.img;
        document.getElementById('status').innerText = "Gedanke erfasst: " + randomCard.name + "?";
        currentState = 'wrong';

        // Bereite Bewegungssensoren vor (iOS 13+ Erlaubnis abfangen)
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

    // Schüttel-Erkennung für den Morph zum Pik-Ass
    function handleMotion(e) {
        let current = e.accelerationIncludingGravity;
        if (!current) return;
        
        let currentTime = new Date().getTime();
        if ((currentTime - lastUpdate) > 100) {
            let diffTime = currentTime - lastUpdate;
            lastUpdate = currentTime;
            
            let speed = Math.abs(current.x + current.y + current.z - lastX - lastY - lastZ) / diffTime * 10000;
            
            if (speed > 500 && currentState === 'wrong') {
                morphToPikAs();
            }
            lastX = current.x;
            lastY = current.y;
            lastZ = current.z;
        }
    }

    function morphToPikAs() {
        currentState = 'pik';
        const cardImg = document.getElementById('card-display');
        
        // Kleine Morph-Animation (Zoom-Effekt)
        cardImg.style.transform = "scale(0) rotate(180deg)";
        setTimeout(() => {
            cardImg.src = pikAsImg;
            cardImg.style.transform = "scale(1) rotate(0deg)";
            document.getElementById('status').innerText = "Fehlerkorrektur: Das Pik-Ass!";
            document.getElementById('arrow-display').classList.remove('hidden');
        }, 300);
    }

    // Handydrehung steuert den Pfeil zur Hose / zum Körper
    function handleOrientation(e) {
        if (currentState !== 'pik') return;
        
        let beta = e.beta;   // Neigung vor/zurück (-180 bis 180)
        let gamma = e.gamma; // Neigung links/rechts (-90 to 90)
        
        const arrow = document.getElementById('arrow-display');
        // Wenn das Handy nach unten geneigt wird, bewegt sich der Pfeil dynamisch
        let moveX = gamma * 1.5;
        let moveY = (beta - 45) * 1.5; // Basisneigung anpassen
        
        arrow.style.transform = `translate(${moveX}px, ${moveY}px)`;
    }
</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=600)
