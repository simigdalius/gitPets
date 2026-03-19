import libsql_client
import os

# Σύνδεση με το Turso (Χρησιμοποίησε Environment Variables στο Render!)
URL = os.getenv("TURSO_DATABASE_URL")
TOKEN = os.getenv("TURSO_AUTH_TOKEN")

def get_db_client():
    return libsql_client.create_client_sync(url=URL, auth_token=TOKEN)

def init_db():
    client = get_db_client()
    # Δημιουργία πίνακα αν δεν υπάρχει
    client.execute("""
        CREATE TABLE IF NOT EXISTS pet_stats (
            username TEXT PRIMARY KEY,
            score INTEGER,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    client.close()

def update_pet_score(username, score):
    client = get_db_client()
    client.execute(
        "INSERT INTO pet_stats (username, score) VALUES (?, ?) "
        "ON CONFLICT(username) DO UPDATE SET score = ?, last_updated = CURRENT_TIMESTAMP",
        (username, score, score)
    )
    client.close()

def get_cached_score(username):
    client = get_db_client()
    result = client.execute("SELECT score FROM pet_stats WHERE username = ?", (username,))
    client.close()
    if result.rows:
        return result.rows[0][0]
    return None
