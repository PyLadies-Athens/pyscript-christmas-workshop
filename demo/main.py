from datetime import datetime
from pyscript import display
from pyodide.ffi import create_proxy 
import js
import random

CHRISTMAS = datetime(2025, 12, 25, 0, 0, 0)

# A list of elegant snowflake designs
SNOWFLAKE_SVGS = [
    "&#10052;",  # ❄
    "&#10053;",  # ❅
    "&#10054;",  # ❆
]

def calculate_countdown():
    now = datetime.now()
    time_difference = CHRISTMAS - now
   
    if time_difference.total_seconds() <= 0:
        js.document.getElementById('countdown').innerHTML = "<h1>🎅 MERRY CHRISTMAS! 🎄</h1>"
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

# 1. Start Countdown Timer (1000ms = 1 second)
proxy_countdown = create_proxy(calculate_countdown)

# 2. Run the function immediately (so the display isn't delayed)
calculate_countdown()

# 3. Use the stable proxy with the native JS timer
js.setInterval(proxy_countdown, 1000)

# 4. Start Snowfall Timer
proxy_snowflake = create_proxy(create_snowflake)
js.setInterval(proxy_snowflake, 300)