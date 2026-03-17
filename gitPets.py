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

@app.route('/api')
def generate_pet():
    username = request.args.get('username')

    if not username:
        username = "Unknown"

    score = get_activity_score(username)

    # 1. Η ΛΟΓΙΚΗ ΜΑΣ: Τώρα διαλέγει ΚΑΙ το σωστό GIF!
    if score > 20:
        status_text = "Super Happy!"
        bg_color = "#4CAF50" # Πράσινο
        gif_path = "happy.gif"
    elif score > 5:
        status_text = "Doing OK!"
        bg_color = "#FFC107" # Κίτρινο
        gif_path = "ok.gif"  # Όταν φτιάξεις το ok.gif, θα το βάλεις στον φάκελο!
    else:
        status_text = "Hungry and Sad..."
        bg_color = "#F44336" # Κόκκινο
        gif_path = "sad.gif" # Εδώ φορτώνει το νέο σου animation!

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
                <stop offset="0%" stop-color="#b8a4c9" />
                <stop offset="100%" stop-color="#594b6d" />
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

        <rect width="300" height="380" fill="url(#plastic-shell)" rx="45" filter="url(#drop-shadow)" stroke="#d3c5e0" stroke-width="2" />
        <path d="M 20 45 Q 150 10 280 45 L 280 70 Q 150 35 20 70 Z" fill="#ffffff" fill-opacity="0.1" />

        <rect x="25" y="40" width="250" height="220" fill="#1a1c23" rx="15" filter="url(#drop-shadow)" />
        <rect x="35" y="50" width="230" height="200" fill="url(#screen-bg)" rx="8" />

        <circle cx="80" cy="315" r="16" fill="#ff7eb3" filter="url(#drop-shadow)" stroke="#d85a8d" stroke-width="2"/>
        <circle cx="150" cy="330" r="16" fill="#ff7eb3" filter="url(#drop-shadow)" stroke="#d85a8d" stroke-width="2"/>
        <circle cx="220" cy="315" r="16" fill="#ff7eb3" filter="url(#drop-shadow)" stroke="#d85a8d" stroke-width="2"/>

        <text x="80" y="285" font-family="'Courier New', monospace" font-size="10" fill="#ffffff" fill-opacity="0.5" text-anchor="middle">FEED</text>
        <text x="150" y="300" font-family="'Courier New', monospace" font-size="10" fill="#ffffff" fill-opacity="0.5" text-anchor="middle">PLAY</text>
        <text x="220" y="285" font-family="'Courier New', monospace" font-size="10" fill="#ffffff" fill-opacity="0.5" text-anchor="middle">CLEAN</text>

        <image x="100" y="60" width="100" height="100" href="{gif_base64}" />
        
        <text x="50%" y="185" font-family="'Courier New', monospace" font-weight="bold" font-size="15" fill="#00ffcc" text-anchor="middle">
            @{username}
        </text>
        
        <text x="50%" y="210" font-family="'Courier New', monospace" font-size="13" fill="#ffffff" text-anchor="middle">
            LVL/SCORE: <tspan fill="#ffeb3b" font-weight="bold">{score}</tspan>
        </text>
        
        <text x="50%" y="235" font-family="'Courier New', monospace" font-weight="bold" font-size="12" fill="{bg_color}" text-anchor="middle">
            > {status_text}_
        </text>
    </svg>
    """

    return Response(svg_image, mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)