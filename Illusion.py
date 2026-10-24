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

        input {
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
            margin-top: 15px;
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 12px;
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
    <div id="input-section" class="input-group">
        <input type="text" id="code-input" placeholder="Code eingeben">
        <button onclick="startMagic()">Analysieren</button>
    </div>

    <div id="magic-section" class="hidden input-group">
        <div id="status">Scanne Frequenz...</div>
        <div class="card-box">
            <img id="card-display" class="card-img" src="" alt="Card">
        </div>
        
        <div id="action-box" class="action-container">
            <button id="find-btn" onclick="showArrow()">Position finden</button>
            <div id="arrow-box" class="arrow-container">
                <svg id="vector-arrow" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <polyline points="19 12 12 19 5 12"></polyline>
                </svg>
            </div>
        </div>
    </div>
</div>

<script>
    const wrongCard = "https://deckofcardsapi.com/static/img/0C.png";
    const rightCard = "https://deckofcardsapi.com/static/img/4S.png";

    let currentState = 'wrong';
    let currentRotation = 0;
    let targetRotation = 0;
    
    let lastX = 0, lastY = 0, lastZ = 0;
    let lastUpdate = 0;

    function startMagic() {
        const code = document.getElementById('code-input').value.trim();
        if(!code) {
            alert("Bitte Code eingeben!");
            return;
        }

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

    function handleMotion(e) {
        if (currentState !== 'wrong') return;
        
        let current = e.accelerationIncludingGravity;
        if (!current) return;
        
        let currentTime = new Date().getTime();
        if ((currentTime - lastUpdate) > 100) {
            let diffTime = currentTime - lastUpdate;
            lastUpdate = currentTime;
            
            let speed = Math.abs(current.x + current.y + current.z - lastX - lastY - lastZ) / diffTime * 10000;
            
            if (speed > 500) {
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
            cardImg.src = rightCard;
            cardImg.style.transform = "scale(1)";
            cardImg.style.opacity = "1";
            document.getElementById('status').innerText = "Matrix korrigiert";
        }, 300);
    }

    function showArrow() {
        document.getElementById('arrow-box').classList.add('visible');
        document.getElementById('find-btn').style.display = 'none';
        document.getElementById('status').innerText = "Standort lokalisiert";
    }

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
                targetRotation *= 0.93;
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
