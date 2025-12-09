# 🎄 PyLadies Athens PyScript Christmas Workshop

## ✨ Final Result

You can see the final result of this workshop in the `demo` directory. You can also see a [Live Demo](https://vadal.pyscriptapps.com/pyladies-athens-christmas-workshop-demo/latest/).

![Christmas Countdown Website](demo/demo.png)

---

In this festive hands-on session, you'll learn how to build a dynamic, animated Christmas Countdown entirely in your web browser using Python and PyScript.

## Goals
By the end of the workshop, you will:
1. ✅ Use **Python logic** to calculate the time remaining until Christmas.
2. ✅ Create **front-end animations** like falling snowflakes using Python and CSS.
3. ✅ Understand how Python can interact with the DOM and bring your web pages to life!

## Before You Begin
This is a hands-on session. Make sure you're ready with:
- 💻 A laptop (Chrome or Firefox browser recommended).
- 📶 Internet access.

We’ll build everything step-by-step. No prior web dev experience needed!

## Accessing the PyScript Web Editor

We’ll use the official PyScript Editor, a browser-based playground where you can run Python + HTML instantly. No installation needed!

- Go to https://pyscript.com
- Sign in using your preferred account
- Visit https://pyscript.com/dashboard
- Create a new project
- You will see the files we are going to work on!

---

## Understanding the Default Code

When you first open the PyScript IDE, your index.html file looks like this:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Plain Base</title>

    <!-- Recommended meta tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">

    <!-- PyScript CSS -->
    <link rel="stylesheet" href="https://pyscript.net/releases/2025.11.1/core.css">

    <!-- This script tag bootstraps PyScript -->
    <script type="module" src="https://pyscript.net/releases/2025.11.1/core.js"></script>
</head>
<body>
    <script type="py" src="./main.py" config="./pyscript.toml" terminal></script>
</body>
</html>
```

Let’s break it down:
- `<link>` and `<script>` inside `<head>` load the PyScript library (CSS and JS) so you can run Python code in the browser.
- `<script type="py" src="./main.py">` tells PyScript to load the Python code from the file main.py.
- `config="./pyscript.toml"` optionally loads settings.
- The terminal attribute makes a Python terminal appear at the bottom of your webpage. We'll keep it for debugging purposes.

You don't need to change this base. You’ll just add your content (countdown and styling) around it!

---

## Workshop Flow

We'll structure our work based on files and what they do:

1. `index.html`: The structure and style of your web page.
2. `main.py`: All the countdown logic and snowflake animation.
3. CSS to make it look beautiful.
4. Bonus challenges if you finish early.

---

### Part 1: Modify Your HTML (index.html)
Your HTML file is already populated with the necessary tags and PyScript setup. 
All you need to do is to open it and add this inside the `<body>` tag, just above the `<script type="py">` line:

```html
<div class="container">
    <h1>🎄 Days 'til Christmas</h1>
    <div id="countdown">
        <div class="timer-box">
            <div id="days" class="timer-value">0</div>
            <div class="timer-label">Days</div>
        </div>
        <div class="timer-box">
            <div id="hours" class="timer-value">0</div>
            <div class="timer-label">Hours</div>
        </div>
        <div class="timer-box">
            <div id="minutes" class="timer-value">0</div>
            <div class="timer-label">Minutes</div>
        </div>
        <div class="timer-box">
            <div id="seconds" class="timer-value">0</div>
            <div class="timer-label">Seconds</div>
        </div>
    </div>
</div>

<footer>
    <p>A gift from <a href="https://linktr.ee/pyladiesathens" target="_blank">PyLadies Athens</a></p>
</footer>
<div id="snow-layer"></div>
```

This creates the main container for our countdown, the countdown display itself with boxes for days, hours, minutes and seconds, a footer and a layer for the snow.

#### Add a Festive Font
To make our countdown more festive, we'll use a special font from Google Fonts called "Mountains of Christmas". Add the following lines inside the `<head>` tag of your `index.html` file:

```html
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Mountains+of+Christmas:wght@400;700&display=swap" rel="stylesheet">
```

---

Then hit **Save** and **▶ Run**. You won’t see the countdown working yet, but the page layout is ready.

### Part 2: Python Logic (main.py)
Now open the main.py tab.

Delete anything that’s there, and paste this code block by block:

#### A. Add the imports
Start by setting up the necessary imports. The create_proxy function is the crucial fix for ensuring stable, non-blocking timers in PyScript.

```python
from datetime import datetime
from pyscript import display
from pyodide.ffi import create_proxy 
import js
import random
```
#### B. Add the Christmas date
```python
CHRISTMAS = datetime(2025, 12, 25, 0, 0, 0)
countdown_interval = None
```

#### C. Add the countdown logic
Next, define the function that runs every second. It calculates the time difference and uses integer division (//) and modulo (%) to break it down into days, hours, minutes, and seconds.
```python
def calculate_countdown():
    global countdown_interval
    now = datetime.now()
    time_difference = CHRISTMAS - now
   
    if time_difference.total_seconds() <= 0:
        js.clearInterval(countdown_interval)
        container = js.document.querySelector('.container')
        container.innerHTML = "<h1>🎅 MERRY CHRISTMAS! 🎄</h1>"
        return 

    days = time_difference.days
    seconds_remainder = time_difference.seconds
    
    hours = seconds_remainder // 3600
    seconds_after_hours = seconds_remainder % 3600 
    
    minutes = seconds_after_hours // 60
    seconds = seconds_after_hours % 60
    
    js.document.getElementById('days').innerHTML = str(days)
    js.document.getElementById('hours').innerHTML = f"{hours:02}"
    js.document.getElementById('minutes').innerHTML = f"{minutes:02}"
    js.document.getElementById('seconds').innerHTML = f"{seconds:02}"
```
#### D. Add the snowflake animation logic
This function generates a new snowflake element, assigns it random properties (position, size, speed, opacity), and injects it into the body of the HTML page. We'll also define a list of snowflake icons to use.

```python
# A list of more elegant snowflake designs
SNOWFLAKE_SVGS = [
    "&#10052;",  # ❄
    "&#10053;",  # ❅
    "&#10054;",  # ❆
]

def create_snowflake():
    # 1. Randomness for position, size, and speed
    start_left = random.randint(1, 99) # Random position (1 to 99)
    duration = random.randint(8, 20)   # Random speed in seconds (8 to 20)
    initial_opacity = random.uniform(0.5, 1) # Random initial opacity

    # 2. Create Element and Apply Styles
    snowflake = js.document.createElement("span")
    snowflake.className = "snowflake" # Applies base styles from <style>
    snowflake.innerHTML = random.choice(SNOWFLAKE_SVGS)

    # 3. Apply random CSS properties
    snowflake.style.left = f"{start_left}%"
    snowflake.style.opacity = initial_opacity
    snowflake.style.fontSize = f"{random.randint(15, 25)}px"


    # 4. Set the 'fall' animation with random speed, linking to our CSS @keyframes
    snowflake.style.animation = f"fall {duration}s linear infinite" 

    # 5. Inject into the body
    js.document.body.appendChild(snowflake)
```

#### E. Start the timers
Finally, we set the recurring timers. We must use `create_proxy()` to ensure that the Python functions (`calculate_countdown` and `create_snowflake`) are correctly passed to the native JavaScript setInterval function, guaranteeing stability.

```python
# 1. Start Countdown Timer (1000ms = 1 second)
proxy_countdown = create_proxy(calculate_countdown)

# 2. Run the function immediately (so the display isn't delayed)
calculate_countdown()

# 3. Use the stable proxy with the native JS timer
countdown_interval = js.setInterval(proxy_countdown, 1000)

# 4. Start Snorflall Timer
proxy_snowflake = create_proxy(create_snowflake)
js.setInterval(proxy_snowflake, 300)
```

Now hit **▶ Run**. You should see the countdown updating every second and ❄️appearing, but it will look pretty plain.

### Part 3: Make It Pretty with CSS
Let’s add the styling! Go back to index.html, and inside the `<head>` tag, just before `</head>`, add:
```html
<style>
    body {
        background: radial-gradient(ellipse at center, #1a2a6c 0%, #000033 70%);
        color: white;
        min-height: 100vh;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-family: 'Mountains of Christmas', cursive;
    }

    .container {
        text-align: center;
        background: #020634;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
        position: relative;
        z-index: 1;
    }
    
    h1 {
        font-size: 4em;
        font-weight: 700;
        margin-bottom: 0.5em;
    }

    #countdown {
        display: flex;
        gap: 1rem;
    }

    .timer-box {
        background: rgba(0, 0, 0, 0.5);
        padding: 1rem;
        border-radius: 10px;
        min-width: 100px;
    }

    .timer-value {
        font-size: 3em;
        font-weight: 700;
    }

    .timer-label {
        font-size: 1em;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.7);
    }
    
    footer {
        position: absolute;
        bottom: 30px;
        font-size: 0.8em;
        color: rgba(255, 255, 255, 0.5);
    }

    footer a {
        color: rgba(255, 255, 255, 0.7);
        text-decoration: none;
    }

    @keyframes fall {
        from {
            top: -10%; 
            opacity: 1;
        }
        to {
            top: 100%;
            opacity: 0;
        }
    }

    .snowflake {
        position: absolute;
        z-index: -1;
        filter: blur(1px);
    }

    #snow-layer {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 10px;
        background: white;
        box-shadow: 0 0 20px 10px white;
        filter: blur(3px);
    }
</style>
```
Now hit **Save** and **▶ Run** again. Your app will look polished and wintry ❄️.

---

**Congratulations!** You have successfully completed the PyLadies Athens PyScript Christmas Workshop. You are now running an animated, real-time countdown entirely powered by Python in your browser.

---
### Bonus Challenges (Optional)

Try these if you have time:

- 🎂 Change the countdown to your birthday
- 🌈 Change the background color every 5 minutes using Python
- ⭐ Use different emojis instead of ❄️
- ⏱️ Let users input their own countdown date

---
### Troubleshooting
| Problem                  | Tip                                                            |
|--------------------------|----------------------------------------------------------------|
| Nothing happens          | Check if you clicked ▶ Run                                     |
| Countdown doesn’t change | Check if the date is still in the future                       |
| Snowflakes don’t fall    | Double-check the CSS @keyframes and .snowflake style           |
