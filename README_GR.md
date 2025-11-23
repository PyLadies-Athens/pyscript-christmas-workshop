# 🎄 PyLadies Athens PyScript Χριστουγεννιάτικο Workshop

Σε αυτό το γιορτινό, πρακτικό workshop θα μάθεις να φτιάχνεις ένα δυναμικό, animated Christmas Countdown απευθείας στον browser σου, χρησιμοποιώντας Python και PyScript.

## Στόχος
Μέχρι το τέλος του workshop θα μπορείς να:
1. ✅ Χρησιμοποιείς **Python** για να υπολογίζεις τον χρόνο που απομένει μέχρι τα Χριστούγεννα.
2. ✅ Υλοποιείς σταθερό timer ενός δευτερολέπτου με `create_proxy` ώστε να αποφύγεις προβλήματα χρονισμού στο PyScript.
3. ✅ Δημιουργείς **front-end animations** (π.χ. νιφάδες χιονιού) με Python και CSS.
4. ✅ Κατανοείς πώς η Python αλληλεπιδρά με τις ιστοσελίδες και τις «ζωντανεύει» !

## Πριν ξεκινήσεις
Πρόκειται για hands-on workshop. Βεβαιώσου ότι έχεις:
- 💻 Ένα laptop (προτείνεται Chrome ή Firefox browser).
- 📶 Πρόσβαση στο διαδίκτυο (το PyScript φορτώνει από CDN).

Θα χτίσουμε το project βήμα-βήμα. Δεν απαιτείται προηγούμενη εμπειρία σε web development!

## Πρόσβαση στον Web Editor του PyScript

Θα χρησιμοποιήσουμε τον επίσημο PyScript Editor, ένα browser-based playground όπου τρέχεις Python + HTML άμεσα, χωρίς εγκατάσταση.

- Μπες στο https://pyscript.com
- Κάνε sign-in με τον λογαριασμό που προτιμάς
- Επισκέψου το https://pyscript.com/dashboard
- Δημιούργησε νέο project
- Θα δεις τα αρχεία με τα οποία θα δουλέψουμε!

---

## Κατανόηση του Default Κώδικα

Όταν ανοίξεις για πρώτη φορά το PyScript IDE, το αρχείο `index.html` φαίνεται έτσι:

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

Ας το δούμε βήμα-βήμα:
- Τα `<link>` και `<script>` μέσα στο `<head>` φορτώνουν το PyScript (CSS και JS) ώστε να τρέχει Python στον browser σου.
- Το `<script type="py" src="./main.py">` λέει στο PyScript να φορτώσει κώδικα Python από το `main.py`.
- Το `config="./pyscript.toml"` προαιρετικά φορτώνει τις ρυθμίσεις για την Python.
- To `terminal` εμφανίζει ένα Python terminal στο κάτω μέρος της σελίδας (χρήσιμο για debugging).

Δεν χρειάζεται να αλλάξεις τα default. Απλώς θα προσθέσεις το περιεχόμενό σου (countdown και styling) γύρω της!

---

## Ροή Workshop

Θα οργανώσουμε τη δουλειά μας ανά αρχείο και ρόλο:

1. `index.html`: Η δομή και το στιλ της σελίδας.
2. `main.py`: Η λογική του countdown και το animation των νιφάδων.
3. CSS για να φαίνεται όμορφο.
4. Bonus προκλήσεις αν τελειώσεις νωρίς.

---

### Μέρος 1: Τροποποίηση HTML (index.html)
Το `index.html` είναι ήδη έτοιμο με τα απαραίτητα tags και το PyScript setup.
Άνοιξέ το και μέσα στο `<body>`, ακριβώς πάνω από τη γραμμή με το `<script type="py">`, πρόσθεσε:

```html
<h1>🎄 Days 'til Christmas</h1>
<div id="countdown">Loading countdown...</div>
```

Αυτό δημιουργεί τον τίτλο και το placeholder όπου θα εμφανίζεται το countdown.

Πάτησε **▶ Run**. Το countdown ακόμα δεν λειτουργεί, αλλά το layout είναι έτοιμο.

### Μέρος 2: Python Λογική (main.py)
Άνοιξε το `main.py`.

Διάγραψε ό,τι υπάρχει και επικόλλησε βήμα-βήμα τον παρακάτω κώδικα:

#### A. Add the imports
Θα φορτώσουμε τα βασικά για να τρέχει Python στον browser. Θα προσθέσουμε και το «fix» με `create_proxy` για σταθερά timers.

```python
from datetime import datetime
from pyscript import display
from pyodide.ffi import create_proxy 
import js
import random
```
#### B. Προσθήκη ημερομηνίας Χριστουγέννων
```python
CHRISTMAS = datetime(2025, 12, 25, 0, 0, 0)
```

#### C. Προσθήκη της λογικής για την αντίστροφη μέτρηση

Στη συνέχεια, ορίζουμε τη συνάρτηση που τρέχει κάθε δευτερόλεπτο, υπολογίζει τη διαφορά με την τωρινή ημερομηνία/ώρα και τη «σπάει» σε μέρες/ώρες/λεπτά/δευτερόλεπτα.

```python
def calculate_countdown():
    now = datetime.now()
    time_difference = CHRISTMAS - now
   
    # 1. Check if Christmas is here
    if time_difference.total_seconds() <= 0:
        display("🎅 MERRY CHRISTMAS! 🎄", target="countdown")
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
#### D. Προσθήκη λογικής για τις νιφάδες χιονιού

Αυτή η συνάρτηση, δημιουργεί νέο element νιφάδας στο DOM, του δίνει τυχαίες ιδιότητες (θέση, μέγεθος, ταχύτητα) και το εισάγει στο body της σελίδας.

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

#### E. Εκκίνηση των timers
Τέλος, σετάρουμε τους επαναλαμβανόμενους timers. Χρησιμοποιούμε το `create_proxy()` για να περάσουμε σωστά τις Python συναρτήσεις στο setInterval της JavaScript.

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

Πάτησε **▶ Run**. Θα δεις το countdown να ανανεώνεται κάθε δευτερόλεπτο και τις ❄️να εμφανίζονται. Η εμφάνιση είναι ακόμα πολύ απλή.

### Μέρος 3: Προσθήκη CSS
Ας κάνουμε λίγο styling! Πήγαινε στο `index.html`, και μέσα στο `<head>`, πριν το `</head>`, πρόσθεσε:
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
Πάτησε ξανά **▶ Run**. Η εφαρμογή σου θα δείχνει πια χειμωνιάτικη και γιορτινή ❄️.

---

**Συγχαρητήρια!** Ολοκλήρωσες το PyLadies Athens PyScript Christmas Workshop. Πλέον έχεις φτιάξει ένα πλήρως λειτουργικό animated countdown, φτιαγμένο εξ' ολοκλήρου με Python στον browser σου.

---
### Bonus Προκλήσεις (Προαιρετικές)

Αν έχεις χρόνο, δοκίμασε:

- 🎂 Άλλαξε το countdown στα γενέθλιά σου
- 🌈 Άλλαζε το background color κάθε 5 λεπτά με Python
- ⭐ Βάλε διαφορετικά emojis αντί για ❄️
- ⏱️ Δώσε τη δυνατότητα στον χρήστη να βάζει δική του ημερομηνία

---
### Troubleshooting
| Πρόβλημα                 | Tip                                                            |
|--------------------------|----------------------------------------------------------------|
| Δεν γίνεται τίποτα       | Έλεγξε αν πάτησες ▶ Run                                        |
| Το countdown δεν αλλάζει | Βεβαιώσου ότι η ημερομηνία είναι ακόμη στο μέλλον              |
| Δεν «πέφτουν» νιφάδες    | Έλεγξε τα CSS `@keyframes` και το στιλ της κλάσης `.snowflake` |