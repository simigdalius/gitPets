import requests
import base64
import os
from flask import Flask, request, Response
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

def get_activity_score(username):
    url = f"https://api.github.com/users/{username}/events/public?per_page=100"
    response = requests.get(url)
    
    if response.status_code != 200:
        return 0
        
    events = response.json()
    score = 0
    now = datetime.now(timezone.utc)
    one_week_ago = now - timedelta(days=7)
    
    for event in events:
        created_at_str = event['created_at']
        event_date = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        
        if event_date >= one_week_ago:
            event_type = event['type']
            if event_type == 'PushEvent':
                score += event['payload'].get('size', 1) * 2  
            elif event_type == 'PullRequestEvent':
                score += 5
            elif event_type in ['PullRequestReviewEvent', 'PullRequestReviewCommentEvent']:
                score += 4
            elif event_type in ['IssuesEvent', 'IssueCommentEvent']:
                score += 3
            elif event_type == 'ForkEvent':
                score += 3
            elif event_type == 'DeleteEvent':
                score += 1
            else:
                score += 1
    return score

def get_pet(petname,mood ):
    petmood = {1:"happy", 2:"ok", 3: "sad"}
    #gia na fouleuei prepei na onomazw ta arxeia ws ekseis molly_happy.gif
    filename = f"{petname}_{petmood[mood]}.gif"
    #na gurnaei sto default an den uparxei onoma gia thn wra molly
    if not os.path.exists(filename):
        return f"{petmood[mood]}.gif"
    return filename



@app.route('/api')
def generate_pet():
    username = request.args.get('username')
    petname = request.args.get('petname', 'molly').lower()

    if not username:
        username = "Unknown"


    #auto einai to antistoixw mapping gia na diaxeiristw xrwma konsolas
    pet_styles = {
        "molly": ["#b8a4c9", "#594b6d", "#ff7eb3"],  # Μωβ/Ροζ (Το κλασικό σου)
        "spot": ["#7ec8ff", "#3a5f85", "#4fc3f7"],  # Μπλε στυλ
        "default": ["#0eac13", "#594b6d", "#5eff00"] # Αν δεν βρει το όνομα
    }

    style = pet_styles.get(petname, pet_styles["default"])
    color_top = style[0]
    color_bottom = style[1]
    color_buttons = style[2]
    
    score = get_activity_score(username)

    # 1. Η ΛΟΓΙΚΗ ΜΑΣ: Τώρα διαλέγει ΚΑΙ το σωστό GIF!
    if score > 20:
        status_text = "Super Happy!"
        bg_color = "#4CAF50" 
        mood_id = 1
    elif score > 5:
        status_text = "Doing OK!"
        bg_color = "#FFC107" 
        mood_id = 2
    else:
        status_text = "Hungry and Sad..."
        bg_color = "#F44336" 
        mood_id = 3
    
    gif_path = get_pet(petname,mood_id)

    # 2. Φορτώνουμε το GIF σε Base64
    gif_base64 = ""
    
    if os.path.exists(gif_path):
        with open(gif_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            gif_base64 = f"data:image/gif;base64,{encoded_string}"
    else:
        fallback_path = "ok.gif"
        if os.path.exists(fallback_path):
            with open(fallback_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                gif_base64 = f"data:image/gif;base64,{encoded_string}"

    # 3. Το SVG της Ρετρό Κονσόλας
    svg_image = f"""
    <svg width="300" height="380" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="plastic-shell" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{color_top}" />
                <stop offset="100%" stop-color="{color_bottom}" />
            </linearGradient>

            
            <linearGradient id="screen-bg" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#0f2027" />
                <stop offset="50%" stop-color="#203a43" />
                <stop offset="100%" stop-color="#2c5364" />
            </linearGradient>

            <filter id="drop-shadow">
                <feDropShadow dx="0" dy="6" stdDeviation="4" flood-color="#000000" flood-opacity="0.4"/>
            </filter>
            </defs>

        <rect width="300" height="380" fill="url(#plastic-shell)" rx="45" stroke="#ffffff" stroke-opacity="0.2" stroke-width="2" />
        
        <rect x="25" y="40" width="250" height="220" fill="#1a1c23" rx="15" />
        <rect x="35" y="50" width="230" height="200" fill="url(#screen-bg)" rx="8" />

        <image x="100" y="65" width="100" height="100" href="{gif_base64}" />
        
        <circle cx="80" cy="315" r="16" fill="{color_buttons}" />
        <circle cx="150" cy="330" r="16" fill="{color_buttons}" />
        <circle cx="220" cy="315" r="16" fill="{color_buttons}" />

        <text x="50%" y="185" font-family="'Courier New', monospace" font-weight="bold" font-size="15" fill="#00ffcc" text-anchor="middle">@{username}</text>
        <text x="50%" y="210" font-family="'Courier New', monospace" font-size="11" fill="#ffffff" text-anchor="middle">TYPE: {petname.upper()} | SCORE: {score}</text>
        <text x="50%" y="235" font-family="'Courier New', monospace" font-weight="bold" font-size="12" fill="{bg_color}" text-anchor="middle">> {status_text}_</text>
    </svg>
    """



    return Response(svg_image, mimetype='image/svg+xml')
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
