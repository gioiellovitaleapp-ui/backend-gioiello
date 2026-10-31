import json
import os

QUEUE_FILE = "data/queue_status.json"

def load_queue_status():
    """Charge l'état actuel de la file d'attente depuis le fichier JSON."""
    if not os.path.exists(QUEUE_FILE):
        return {"processed_ids": []}
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"processed_ids": []}

def filter_new_articles(articles):
    """Filtre les articles en se basant sur les identifiants déjà traités."""
    status = load_queue_status()
    processed_ids = set(status.get("processed_ids", []))

    new_items = []
    for art in articles:
        if art["id"] not in processed_ids:
            new_items.append(art)

    return new_items
