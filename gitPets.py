import requests
from flask import Flask, request, Response
# ΝΕΟ: Εισάγουμε τα εργαλεία για τον χρόνο!
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

def get_activity_score(username):
    # Προσθέσαμε το ?per_page=100 για να τραβάει 100 events, ώστε να είμαστε σίγουροι ότι πιάνει όλη την εβδομάδα!
    url = f"https://api.github.com/users/{username}/events/public?per_page=100"
    response = requests.get(url)
    
    if response.status_code != 200:
        return 0
        
    events = response.json()
    score = 0
    
    # 1. Βρίσκουμε την τωρινή ώρα και αφαιρούμε 7 μέρες
    now = datetime.now(timezone.utc)
    one_week_ago = now - timedelta(days=7)
    
    for event in events:
        # 2. Διαβάζουμε την ημερομηνία που έγινε το event στο GitHub
        created_at_str = event['created_at']
        
        # Την μετατρέπουμε από κείμενο σε πραγματικό "Χρόνο" που καταλαβαίνει η Python
        event_date = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        
        # 3. Ελέγχουμε: Έγινε αυτό το event μετά από την προηγούμενη εβδομάδα;
        if event_date >= one_week_ago:
            # Αν ΝΑΙ, τότε δίνουμε τους πόντους κανονικά!
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

    if score > 20:
        status_text = "Super Happy! "
        bg_color = "#4CAF50" # Πράσινο
    elif score > 5:
        status_text = "Doing OK! "
        bg_color = "#FFC107" # Κίτρινο
    else:
        status_text = "Hungry and Sad... "
        bg_color = "#F44336" # Κόκκινο

    # Αλλάξαμε το κείμενο σε "Weekly Score" για να είναι ξεκάθαρο!
    svg_image = f"""
    <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="{bg_color}" rx="15" />
        <text x="50%" y="40%" font-family="Arial" font-size="24" fill="white" text-anchor="middle">
            {username}'s Pet
        </text>
        <text x="50%" y="60%" font-family="Arial" font-size="20" fill="white" text-anchor="middle">
            Weekly Score: {score}
        </text>
        <text x="50%" y="80%" font-family="Arial" font-size="22" fill="white" text-anchor="middle">
            {status_text}
        </text>
    </svg>
    """

    return Response(svg_image, mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)