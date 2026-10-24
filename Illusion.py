import streamlit as st

st.set_page_config(page_title="Magic App", layout="wide", initial_sidebar_state="collapsed")

html_code = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Magic Matrix</title>
    <style>
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
        
        #MainMenu, header, footer { visibility: hidden !important; }

        .container {
            text-align: center;
            width: 100%;
            max-width: 320px;
            padding: 0 20px;
            box-sizing: border-box;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            width: 100%;
        }

        /* Alle Eingabefelder und Buttons exakt gleich groß und symmetrisch */
        input, button {
            width: 100% !important;
            height: 48px !important;
            padding: 0 14px !important;
            font-size: 16px !important;
            border-radius: 10px !important;
            border: 1px solid #27272a !important;
            background: #09090b !important;
            color: #ffffff !important;
            text-align: center !important;
            outline: none !important;
            box-sizing: border-box !important;
            letter-spacing: 1px !important;
            -webkit-appearance: none;
        }

        input::placeholder {
            color: #52525b;
        }

        button {
            background: #18181b !important;
            border: 1px solid #3f3f46 !important;
            cursor: pointer;
            font-weight: 500;
        }

        button:active {
            background: #27272a !important;
        }

        .card-box {
            margin-top: 15px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .card-img {
            width: 150px;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.9);
            transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s ease;
        }

        .code-display {
            margin-top: 12px;
            font-family: monospace;
            font-size: 16px;
            letter-spacing: 2px;
            color: #a1a1aa;
        }

        .arrow-container {
            margin-top: 15px;
            height: 50px;
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
            width: 40px;
            height: 40px;
            filter: drop-shadow(0 2px 8px rgba(56, 189, 248, 0.4));
        }

        .hidden {
            display: none !important;
        }

        #status {
            font-size: 11px;
            color: #71717a;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
    </style>
</head>
<body>

<div class="container">
    <!-- Eingabebereiche -->
    <div id="input-section" class="input-group">
        <input type="number" id="pos-input" placeholder="Position im Deck">
        <input type="date" id="date-input">
        <button onclick="startMagic()">Matrix berechnen</button>
    </div>

    <!-- Magie & Ausgabe -->
    <div id="magic-section" class="hidden input-group">
        <div id="status">Stargazer Frequenz aktiv</div>
        <div class="card-box">
            <img id="card-display" class="card-img" src="" alt="Card">
            <div id="code-text" class="code-display"></div>
        </div>
        
        <!-- Der neue Umformungs-Knopf -->
        <button id="morph-btn" onclick="triggerMorph()">Matrix umformieren</button>

        <div id="arrow-box" class="arrow-container">
            <svg id="vector-arrow" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <polyline points="19 12 12 19 5 12"></polyline>
            </svg>
        </div>
    </div>
</div>

<script>
    // Hochauflösende Visualisierungen der echten Karten
    const cardStargazer = "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400"; // Platzhalter / Echte Stargazer Optik
    const cardArchangels = "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=400"; // Platzhalter / Echte Archangels Optik
    
    // Fallback zu Standard-Karten falls gewünscht, wir nutzen hier die aus den Referenzen bekannten optischen Verhältnisse:
    const realStargazer = "https://deckofcardsapi.com/static/img/AS.png"; 
    const realArchangels = "https://deckofcardsapi.com/static/img/AS.png";

    const wrongCards = [
        "https://deckofcardsapi.com/static/img/0C.png",
        "https://deckofcardsapi.com/static/img/KH.png",
        "https://deckofcardsapi.com/static/img/JD.png"
    ];

    let isMorphAllowed = true;
    let currentRotation = 0;
    let targetRotation = 0;

    function startMagic() {
        const posVal = parseInt(document.getElementById('pos-input').value);
        const dateVal = document.getElementById('date-input').value;
        
        if(isNaN(posVal) || !dateVal) {
            alert("Bitte Position und Geburtsdatum eingeben!");
            return;
        }

        document.getElementById('input-section').classList.add('hidden');
        document.getElementById('magic-section').classList.remove('hidden');

        // Wenn Position > 35: Falsche Karte, kein Umformen möglich
        if (posVal > 35) {
            isMorphAllowed = false;
            let randomWrong = wrongCards[Math.floor(Math.random() * wrongCards.length)];
            document.getElementById('card-display').src = randomWrong;
            document.getElementById('code-text').innerText = "ERR-" + posVal;
            document.getElementById('status').innerText = "Keine Resonanz";
            document.getElementById('morph-btn').style.display = 'none';
            return;
        }

        // Gültiger Bereich (<= 35): Zeigt Stargazer und Code 1219-Z3672
        isMorphAllowed = true;
        document.getElementById('card-display').src = realStargazer;
        document.getElementById('code-text').innerText = "1219-Z3672";
        document.getElementById('status').innerText = "Stargazer Deck";
        
        initSensors();
    }

    function triggerMorph() {
        if (!isMorphAllowed) return;

        const cardImg = document.getElementById('card-display');
        const codeText = document.getElementById('code-text');
        
        cardImg.style.transform = "scale(0.8)";
        cardImg.style.opacity = "0.2";

        setTimeout(() => {
            // Verwandlung in Archangels Code und Karte
            codeText.innerText = "0423-D3396";
            document.getElementById('status').innerText = "Archangels Deck";
            cardImg.src = realArchangels;
            
            cardImg.style.transform = "scale(1)";
            cardImg.style.opacity = "1";
            
            // Verstecke den Knopf nach der Verwandlung und zeige den Pfeil
            document.getElementById('morph-btn').style.display = 'none';
            document.getElementById('arrow-box').classList.add('visible');
        }, 300);
    }

    function initSensors() {
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

    // Tisch-Rotation: Reagiert aufs Drehen und federt sanft zurück
    function handleOrientation(e) {
        let alpha = e.alpha; 
        if (alpha !== null) {
            targetRotation = (alpha % 360) * 0.5;
        }
    }

    function animatePhysics() {
        const arrow = document.getElementById('vector-arrow');
        if (arrow) {
            if (Math.abs(targetRotation - currentRotation) < 0.1) {
                targetRotation *= 0.93; // Federt zurück zur Ausgangsposition beim Anhalten
            }
            
            currentRotation += (targetRotation - currentRotation) * 0.08;
            arrow.style.transform = `rotate(${currentRotation}deg)`;
        }
        requestAnimationFrame(animatePhysics);
    }
    requestAnimationFrame(animatePhysics);
</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=750, scrolling=False)
