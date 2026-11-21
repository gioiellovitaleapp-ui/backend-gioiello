import os
import json
from datetime import datetime
import pytz

STATUS_FILE = "queue_status.json"

# Dictionnaire lexical Bianconero
BIANCONERO_DICTIONARY = {}

def apply_bianconero_dictionary(text):
    """Applique le dictionnaire lexical Bianconero."""
    if not text:
        return text
    for old_term, new_term in BIANCONERO_DICTIONARY.items():
        text = text.replace(old_term, new_term)
    return text

def normalize_timestamp(published_str):
    """Normalise la date sur le fuseau Europe/Rome."""
    rome_tz = pytz.timezone("Europe/Rome")
    try:
        dt = datetime.now(rome_tz)
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    except Exception:
        return datetime.now(rome_tz).strftime("%Y-%m-%d %H:%M:%S %Z%z")

def load_queue_status():
    """Charge l'état actuel de la file d'attente."""
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Erreur de lecture du fichier d'état, réinitialisation...")
            return {}
    return {}

def save_queue_status(status_data):
    """Sauvegarde l'état de la file d'attente."""
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status_data, f, ensure_ascii=False, indent=4)

def filter_new_articles(raw_articles):
    """
    Filtre les nouveaux articles, applique les transformations 
    et met à jour le statut.
    """
    queue_status = load_queue_status()
    new_articles = []

    for article in raw_articles:
        link = article.get("link")
        if not link:
            continue

        if link not in queue_status:
            cleaned_title = apply_bianconero_dictionary(article.get("title"))
            normalized_date = normalize_timestamp(article.get("published"))

            queue_status[link] = {
                "title": cleaned_title,
                "published": normalized_date,
                "status": "pending"
            }
            
            article["title"] = cleaned_title
            article["published"] = normalized_date
            new_articles.append(article)

    save_queue_status(queue_status)
    print(f"File d'attente mise à jour : {len(new_articles)} nouveaux articles ajoutés.")
    return new_articles
