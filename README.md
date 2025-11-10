# 🎄 PyLadies Athens PyScript Christmas Workshop

In this festive hands-on session, you'll learn how to build a dynamic, animated Christmas Countdown entirely in your web browser using Python and PyScript.

## Goals
By the end of the workshop, you will:
1. ✅ Use **Python logic** to calculate the time remaining until Christmas.
2. ✅ Implement a **stable 1-second timer** using `create_proxy` to avoid timing issues in PyScript.
3. ✅ Create **front-end animations** like falling snowflakes using Python and CSS.
4. ✅ Understand how Python can interact with the DOM and bring your web pages to life!

## Before You Begin
This is a hands-on session. Make sure you're ready with:
- 💻 A laptop (Chrome or Firefox browser recommended).
- 📶 Internet access (PyScript loads from CDN).
- Optional: pair up with someone near you!

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
<h1>🎄 Days 'til Christmas</h1>
<div id="countdown">Loading countdown...</div>
```

This creates the heading and the placeholder where we’ll show the countdown.

Then hit **▶ Run**. You won’t see the countdown working yet, but the page layout is ready.

### Part 2: Python Logic (main.py)
Now open the main.py tab.

Delete anything that’s there, and paste this code block by block:

#### A. Imports and Setup

We need to include the PyScript core files to make Python run in the browser. We should also include the Configuration Fix to hide the Python terminal from the webpage.

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
```

#### C. Add the countdown logic
Next, define the function that runs every second. It calculates the time difference and uses integer division (//) and modulo (%) to break it down into days, hours, minutes, and seconds.
```python
def calculate_countdown():
    now = datetime.now()
    time_difference = CHRISTMAS - now
   
    # 1. Check if Christmas is here
    if time_difference.total_seconds() <= 0:
        display("🎅 MERRY CHRISTMAS! 🎄", target="countdown")
        # We could add js.clearInterval here if we wanted to stop the loop
        return 

    # 2. Calculate Days, Hours, Minutes, Seconds
    days = time_difference.days
    seconds_remainder = time_difference.seconds
    
    hours = seconds_remainder // 3600
    seconds_after_hours = seconds_remainder % 3600 
    
    minutes = seconds_after_hours // 60
    seconds = seconds_after_hours % 60
    
    # 3. Format and Display (using :02 to ensure two digits, like 05)
    countdown_text = f"{days} days, {hours:02}h, {minutes:02}m, {seconds:02}s"
    js.document.getElementById('countdown').innerHTML = countdown_text
```
#### D. Add the snowflake animation logic
This function generates a new snowflake element, assigns it random properties (position, size, speed), and injects it into the body of the HTML page.

```python
def create_snowflake():
    # 1. Randomness for position, size, and speed
    start_left = random.randint(1, 99) # Random position (1 to 99)
    duration = random.randint(6, 15)   # Random speed in seconds (6 to 15)

    # 2. Create Element and Apply Styles
    snowflake = js.document.createElement("span")
    snowflake.className = "snowflake" # Applies base styles from <style>
    snowflake.innerHTML = "❄️"

    # 3. Apply random CSS properties
    snowflake.style.left = f"{start_left}%"
    snowflake.style.fontSize = f"{random.randint(10, 24)}px" 

    # 3. Set the 'fall' animation with random speed, linking to our CSS @keyframes
    snowflake.style.animation = f"fall {duration}s linear infinite" 

    # 4. Inject into the body
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
js.setInterval(proxy_countdown, 1000)

# 4. Start Snorflall Timer
proxy_snowflake = create_proxy(create_snowflake)
js.setInterval(proxy_snowflake, 300)
```

Now hit **▶ Run**. You should see the countdown updating every second and ❄️appearing, but it will look pretty plain.

### Part 3: Make It Pretty with CSS
Let’s add the styling! Go back to index.html, and inside the <head> tag, just before </head>, add:
```html
<style>
    body {
        background: #000033; /* Dark blue background */
        color: white;
        min-height: 100vh;
        overflow: hidden; /* Hide the scrollbar caused by falling elements */
    }
    
    #countdown {
        font-size: 2em; 
        font-weight: bold; 
        margin: 20px;
    }
    
    /* Define the 'fall' animation */
    @keyframes fall {
        /* Start the snowflake slightly above the viewport */
        from {
            top: -10%; 
            opacity: 1;
        }
        
        /* End the snowflake below the viewport and fade it out */
        to {
            top: 100%;
            opacity: 0; /* Fade out as it hits the bottom */
        }
    }

    /* 2. Style for the snowflake element */
    .snowflake {
        position: absolute;
        z-index: 1000;      /* Ensure they float above other content */
        
        /* Initially hide it, as Python will apply the animation property */
        animation-name: none; 
    }
</style>
```
Now hit **▶ Run** again. Your app will look polished and wintry ❄️.

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