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
            transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s ease;
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

<div class="container">
    <!-- Step 1: Geheime Kartenauswahl mit Bestätigungs-Button -->
    <div id="setup-section" class="input-group">
        <div id="status">Geheimes Setup</div>
        <select id="secret-card-select">
            <!-- Pik -->
            <option value="AS">Pik Ass (PA)</option>
            <option value="2S">Pik 2</option>
            <option value="3S">Pik 3</option>
            <option value="4S">Pik 4</option>
            <option value="5S">Pik 5</option>
            <option value="6S">Pik 6</option>
            <option value="7S">Pik 7</option>
            <option value="8S">Pik 8</option>
            <option value="9S">Pik 9</option>
            <option value="0S">Pik 10</option>
            <option value="JS">Pik Bube (PB)</option>
            <option value="QS">Pik Dame (PD)</option>
            <option value="KS">Pik König (PK)</option>
            <!-- Herz -->
            <option value="AH">Herz Ass (HA)</option>
            <option value="2H">Herz 2</option>
            <option value="3H">Herz 3</option>
            <option value="4H">Herz 4</option>
            <option value="5H">Herz 5</option>
            <option value="6H">Herz 6</option>
            <option value="7H">Herz 7</option>
            <option value="8H">Herz 8</option>
            <option value="9H">Herz 9</option>
            <option value="0H">Herz 10</option>
            <option value="JH">Herz Bube (HB)</option>
            <option value="QH">Herz Dame (HD)</option>
            <option value="KH">Herz König (HK)</option>
            <!-- Kreuz -->
            <option value="KC">Kreuz König (KK)</option>
            <option value="QC">Kreuz Dame (KD)</option>
            <option value="JC">Kreuz Bube (KB)</option>
            <option value="0C">Kreuz 10</option>
            <option value="9C">Kreuz 9</option>
            <option value="8C">Kreuz 8</option>
            <option value="7C">Kreuz 7</option>
            <option value="6C">Kreuz 6</option>
            <option value="5C">Kreuz 5</option>
            <option value="4C">Kreuz 4</option>
            <option value="3C">Kreuz 3</option>
            <option value="2C">Kreuz 2</option>
            <option value="AC">Kreuz Ass (KA)</option>
            <!-- Karo -->
            <option value="KD">Karo König</option>
            <option value="QD">Karo Dame</option>
            <option value="JD">Karo Bube</option>
            <option value="0D">Karo 10</option>
            <option value="9D">Karo 9</option>
            <option value="8D">Karo 8</option>
            <option value="7D">Karo 7</option>
            <option value="6D">Karo 6</option>
            <option value="5D">Karo 5</option>
            <option value="4D">Karo 4</option>
            <option value="3D">Karo 3</option>
            <option value="2D">Karo 2</option>
            <option value="AD">Karo Ass</option>
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
        <div id="status-perf">Scanne Frequenz...</div>
        <div class="card-box">
            <img id="card-display" class="card-img" src="" alt="Card">
        </div>
        
        <div class="action-container">
            <button id="find-btn" onclick="showLocation()" class="hidden">Position finden</button>
            <div id="location-text" class="reveal-text">
                Die Karte ist im Geldbeutel
            </div>
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

    const wrongCard = "https://deckofcardsapi.com/static/img/0C.png";
    let targetCardApi = "AS";
    let currentState = 'wrong';
    
    let lastX = 0, lastY = 0, lastZ = 0;
    let lastUpdate = 0;

    // Schritt 1: Karte bestätigen und zur Code-Eingabe wechseln
    function confirmCard() {
        targetCardApi = document.getElementById('secret-card-select').value;
        document.getElementById('setup-section').classList.add('hidden');
        document.getElementById('input-section').classList.remove('hidden');
    }

    // Schritt 2: Code eingeben und Performance starten
    function startMagic() {
        const codeInput = document.getElementById('code-input').value.trim().toUpperCase();
        
        if(!cardDatabase[codeInput]) {
            alert("Ungültiger Code! Bitte einen Code aus deiner Liste eingeben.");
            return;
        }

        // Optional: Abgleich, ob der eingegebene Code zur gewählten Karte passt (oder direkt übernehmen)
        targetCardApi = cardDatabase[codeInput];

        document.getElementById('input-section').classList.add('hidden');
        document.getElementById('magic-section').classList.remove('hidden');

        document.getElementById('card-display').src = wrongCard;
        currentState = 'wrong';

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
            
            if (speed > 400) {
                morphCard();
            }
            lastX = current.x;
            lastY = current.y;
            lastZ = current.z;
        }
    }

    function morphCard() {
        currentState = 'right';
        const cardImg = document.getElementById('card-display');
        
        cardImg.style.transform = "scale(0.8)";
        cardImg.style.opacity = "0.2";

        setTimeout(() => {
            cardImg.src = `https://deckofcardsapi.com/static/img/${targetCardApi}.png`;
            cardImg.style.transform = "scale(1)";
            cardImg.style.opacity = "1";
            document.getElementById('status-perf').innerText = "Matrix korrigiert";
            
            document.getElementById('find-btn').classList.remove('hidden');
        }, 300);
    }

    function showLocation() {
        document.getElementById('find-btn').classList.add('hidden');
        const locationText = document.getElementById('location-text');
        locationText.classList.add('visible');
        document.getElementById('status-perf').innerText = "Standort lokalisiert";
    }
</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=750, scrolling=False)
