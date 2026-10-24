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

        /* Unsichtbarer Schalter oben links */
        .secret-toggle {
            position: fixed;
            top: 10px;
            left: 10px;
            width: 40px;
            height: 40px;
            z-index: 999;
            opacity: 0.01;
            cursor: pointer;
        }

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

        select, input {
            width: 100% !important;
            height: 48px !important;
            padding: 0 14px !important;
            font-size: 15px !important;
            border-radius: 10px !important;
            border: 1px solid #27272a !important;
            background: #09090b !important;
            color: #ffffff !important;
            text-align: center !important;
            outline: none !important;
            box-sizing: border-box !important;
            -webkit-appearance: none;
        }

        select {
            text-align-last: center;
        }

        input::placeholder {
            color: #52525b;
        }

        button {
            width: 100% !important;
            height: 48px !important;
            padding: 0 14px !important;
            font-size: 16px !important;
            border-radius: 10px !important;
            border: 1px solid #3f3f46 !important;
            background: #18181b !important;
            cursor: pointer;
            font-weight: 500;
            color: #ffffff !important;
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
            transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275), filter 0.8s ease, opacity 0.5s ease;
        }

        /* Wackel-Effekt während des Schüttelns */
        @keyframes shakeCard {
            0% { transform: translate(0, 0) rotate(0deg); }
            20% { transform: translate(-3px, 3px) rotate(-2deg); }
            40% { transform: translate(3px, -2px) rotate(2deg); }
            60% { transform: translate(-2px, -3px) rotate(-1deg); }
            80% { transform: translate(3px, 3px) rotate(2deg); }
            100% { transform: translate(0, 0) rotate(0deg); }
        }

        .shaking {
            animation: shakeCard 0.15s infinite ease-in-out;
        }

        /* Visueller Morphing-Effekt zur Zielkarte */
        .morphing {
            transform: scale(0.4) rotate(15deg);
            filter: blur(12px) brightness(1.8);
            opacity: 0.1;
        }

        .action-container {
            margin-top: 20px;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }

        .reveal-text {
            font-size: 18px;
            font-weight: 500;
            letter-spacing: 1px;
            color: #e4e4e7;
            display: none;
            opacity: 0;
            transform: translateY(10px);
            transition: opacity 0.6s ease, transform 0.6s ease;
            margin-top: 15px;
        }

        .reveal-text.visible {
            display: block;
            opacity: 1;
            transform: translateY(0);
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

    <!-- Unsichtbarer Schalter oben links -->
    <div class="secret-toggle" onclick="toggleScreen()" title="Switch"></div>

<div class="container">
    <!-- Step 1: Geheimes Setup -->
    <div id="setup-section" class="input-group">
        <div id="status">Geheimes Setup</div>
        
        <select id="secret-card-select">
            <option value="1219-Z3672">Pik Ass (PA)</option>
            <option value="1219-Z3673">Pik 2</option>
            <option value="1219-Z3674">Pik 3</option>
            <option value="1219-Z3675">Pik 4</option>
            <option value="1219-Z3676">Pik 5</option>
            <option value="1219-Z3677">Pik 6</option>
            <option value="1219-Z3678">Pik 7</option>
            <option value="1219-Z3679">Pik 8</option>
            <option value="1219-Z3680">Pik 9</option>
            <option value="1219-Z3681">Pik 10</option>
            <option value="1219-Z3682">Pik Bube (PB)</option>
            <option value="1219-Z3683">Pik Dame (PD)</option>
            <option value="1219-Z3684">Pik König (PK)</option>
            <option value="1219-Z3685">Herz Ass (HA)</option>
            <option value="1219-Z3686">Herz 2</option>
            <option value="1219-Z3687">Herz 3</option>
            <option value="1219-Z3688">Herz 4</option>
            <option value="1219-Z3689">Herz 5</option>
            <option value="1219-Z3690">Herz 6</option>
            <option value="1219-Z3691">Herz 7</option>
            <option value="1219-Z3692">Herz 8</option>
            <option value="1219-Z3693">Herz 9</option>
            <option value="1219-Z3694">Herz 10</option>
            <option value="1219-Z3695">Herz Bube (HB)</option>
            <option value="1219-Z3696">Herz Dame (HD)</option>
            <option value="1219-Z3697">Herz König (HK)</option>
            <option value="1219-Z3698">Kreuz König (KK)</option>
            <option value="1219-Z3699">Kreuz Dame (KD)</option>
            <option value="1219-Z3700">Kreuz Bube (KB)</option>
            <option value="1219-Z3701">Kreuz 10</option>
            <option value="1219-Z3702">Kreuz 9</option>
            <option value="1219-Z3703">Kreuz 8</option>
            <option value="1219-Z3704">Kreuz 7</option>
            <option value="1219-Z3705">Kreuz 6</option>
            <option value="1219-Z3706">Kreuz 5</option>
            <option value="1219-Z3707">Kreuz 4</option>
            <option value="1219-Z3708">Kreuz 3</option>
            <option value="1219-Z3709">Kreuz 2</option>
            <option value="1219-Z3710">Kreuz Ass (KA)</option>
            <option value="1219-Z3711">Karo König</option>
            <option value="1219-Z3712">Karo Dame</option>
            <option value="1219-Z3713">Karo Bube</option>
            <option value="1219-Z3714">Karo 10</option>
            <option value="1219-Z3715">Karo 9</option>
            <option value="1219-Z3716">Karo 8</option>
            <option value="1219-Z3717">Karo 7</option>
            <option value="1219-Z3718">Karo 6</option>
            <option value="1219-Z3719">Karo 5</option>
            <option value="1219-Z3720">Karo 4</option>
            <option value="1219-Z3721">Karo 3</option>
            <option value="1219-Z3722">Karo 2</option>
            <option value="1219-Z3723">Karo Ass</option>
        </select>

        <!-- Satz-Auswahl -->
        <select id="secret-sentence-select">
            <option value="Die Karte ist im Geldbeutel">Die Karte ist im Geldbeutel</option>
            <option value="Die Karte ist in deiner Tasche">Die Karte ist in deiner Tasche</option>
            <option value="Die Karte ist in meiner Tasche">Die Karte ist in meiner Tasche</option>
        </select>

        <button onclick="confirmCard()">Karte bestätigen</button>
    </div>

    <!-- Step 2: Code-Eingabe -->
    <div id="input-section" class="input-group hidden">
        <div id="status-input">Bereit für Eingabe</div>
        <input type="text" id="code-input" placeholder="Code eingeben (z.B. 1219-Z3672)">
        <button onclick="startMagic()">Analysieren</button>
    </div>

    <!-- Step 3: Magic Execution Screen -->
    <div id="magic-section" class="hidden input-group">
        <div id="status-perf">Analysiere Schwingung...</div>
        <div class="card-box">
            <img id="card-display" class="card-img" src="" alt="Card">
        </div>
        
        <div class="action-container">
            <button id="find-btn" onclick="showLocation()" class="hidden">Position finden</button>
            <div id="location-text" class="reveal-text"></div>
        </div>
    </div>
</div>

<script>
    const cardDatabase = {
        "1219-Z3672": "AS", "1219-Z3673": "2S", "1219-Z3674": "3S", "1219-Z3675": "4S",
        "1219-Z3676": "5S", "1219-Z3677": "6S", "1219-Z3678": "7S", "1219-Z3679": "8S",
        "1219-Z3680": "9S", "1219-Z3681": "0S", "1219-Z3682": "JS", "1219-Z3683": "QS", "1219-Z3684": "KS",
        "1219-Z3685": "AH", "1219-Z3686": "2H", "1219-Z3687": "3H", "1219-Z3688": "4H",
        "1219-Z3689": "5H", "1219-Z3690": "6H", "1219-Z3691": "7H", "1219-Z3692": "8H",
        "1219-Z3693": "9H", "1219-Z3694": "0H", "1219-Z3695": "JH", "1219-Z3696": "QH", "1219-Z3697": "KH",
        "1219-Z3698": "KC", "1219-Z3699": "QC", "1219-Z3700": "JC", "1219-Z3701": "0C",
        "1219-Z3702": "9C", "1219-Z3703": "8C", "1219-Z3704": "7C", "1219-Z3705": "6C",
        "1219-Z3706": "5C", "1219-Z3707": "4C", "1219-Z3708": "3C", "1219-Z3709": "2C", "1219-Z3710": "AC",
        "1219-Z3711": "KD", "1219-Z3712": "QD", "1219-Z3713": "JD", "1219-Z3714": "0D",
        "1219-Z3715": "9D", "1219-Z3716": "8D", "1219-Z3717": "7D", "1219-Z3718": "6D",
        "1219-Z3719": "5D", "1219-Z3720": "4D", "1219-Z3721": "3D", "1219-Z3722": "2D", "1219-Z3723": "AD"
    };

    const randomWrongCards = [
        "https://deckofcardsapi.com/static/img/0C.png",
        "https://deckofcardsapi.com/static/img/5H.png",
        "https://deckofcardsapi.com/static/img/2S.png",
        "https://deckofcardsapi.com/static/img/KD.png"
    ];

    let targetCardApi = "AS";
    let selectedSentence = "Die Karte ist im Geldbeutel";
    let currentState = 'wrong';
    
    let lastX = 0, lastY = 0, lastZ = 0;
    let lastUpdate = 0;
    let shakeProgress = 0;

    function toggleScreen() {
        const setupSec = document.getElementById('setup-section');
        const inputSec = document.getElementById('input-section');
        const magicSec = document.getElementById('magic-section');

        if (!setupSec.classList.contains('hidden')) {
            setupSec.classList.add('hidden');
            inputSec.classList.remove('hidden');
            document.getElementById('status-input').innerText = "Bereit für Eingabe";
        } else {
            inputSec.classList.add('hidden');
            magicSec.classList.add('hidden');
            setupSec.classList.remove('hidden');
        }
    }

    function confirmCard() {
        const selectedCode = document.getElementById('secret-card-select').value;
        targetCardApi = cardDatabase[selectedCode];
        selectedSentence = document.getElementById('secret-sentence-select').value;

        navigator.clipboard.writeText(selectedCode).catch(err => console.error(err));

        document.getElementById('setup-section').classList.add('hidden');
        document.getElementById('input-section').classList.remove('hidden');
        document.getElementById('status-input').innerText = "Bereit für Eingabe";
    }

    function startMagic() {
        const codeInput = document.getElementById('code-input').value.trim().toUpperCase();
        
        if(!cardDatabase[codeInput]) {
            alert("Ungültiger Code!");
            return;
        }

        targetCardApi = cardDatabase[codeInput];

        document.getElementById('input-section').classList.add('hidden');
        document.getElementById('magic-section').classList.remove('hidden');

        const randomStart = randomWrongCards[Math.floor(Math.random() * randomWrongCards.length)];
        const cardImg = document.getElementById('card-display');
        cardImg.src = randomStart;
        cardImg.classList.remove('morphing');
        
        currentState = 'wrong';
        shakeProgress = 0;

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
    }

    function handleMotion(e) {
        if (currentState !== 'wrong') return;
        
        let current = e.accelerationIncludingGravity;
        if (!current) return;
        
        let currentTime = new Date().getTime();
        if ((currentTime - lastUpdate) > 100) {
            let diffTime = currentTime - lastUpdate;
            lastUpdate = currentTime;
            
            let speed = Math.abs(current.x + current.y + current.z - lastX - lastY - lastZ) / diffTime * 10000;
            const cardImg = document.getElementById('card-display');

            if (speed > 350) {
                shakeProgress += 1;
                // Karte fängt an zu wackeln beim Schütteln
                cardImg.classList.add('shaking');
                
                // ca. 3-4 Sekunden kontinuierliches Schütteln
                if (shakeProgress >= 18) {
                    cardImg.classList.remove('shaking');
                    morphCard();
                }
            } else {
                // Wenn kurz nicht geschüttelt wird, Wackeln langsam beruhigen
                if(shakeProgress > 0) {
                    shakeProgress = Math.max(0, shakeProgress - 0.5);
                    if(shakeProgress === 0) cardImg.classList.remove('shaking');
                }
            }
            lastX = current.x;
            lastY = current.y;
            lastZ = current.z;
        }
    }

    function morphCard() {
        currentState = 'right';
        const cardImg = document.getElementById('card-display');
        
        // Visueller Morphing-Effekt (Startkarte schrumpft & verschwimmt)
        cardImg.classList.add('morphing');

        setTimeout(() => {
            // Bild zur Zielkarte wechseln während sie unscharf/klein ist
            cardImg.src = `https://deckofcardsapi.com/static/img/${targetCardApi}.png`;
            
            // Zurück in Normalgröße morphen
            cardImg.classList.remove('morphing');
            document.getElementById('status-perf').innerText = "Bereit";
            
            document.getElementById('find-btn').classList.remove('hidden');
        }, 400);
    }

    function showLocation() {
        document.getElementById('find-btn').classList.add('hidden');
        const locationText = document.getElementById('location-text');
        locationText.innerText = selectedSentence;
        locationText.classList.add('visible');
    }
</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=750, scrolling=False)
