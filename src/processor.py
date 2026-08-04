import os
import json

STATUS_FILE = "queue_status.json"

def load_queue_status():
    """Charge l'état actuel de la file d'attente depuis le fichier JSON."""
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Erreur de lecture du fichier d'état, réinitialisation...")
            return {}
    return {}

def save_queue_status(status_data):
    """Sauvegarde l'état de la file d'attente dans le fichier JSON."""
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status_data, f, ensure_ascii=False, indent=4)

def filter_new_articles(raw_articles):
    """
    Filtre les articles reçus par rapport à la base d'état existante.
    Enregistre les nouveaux articles avec le statut 'pending'.
    """
    queue_status = load_queue_status()
    new_articles = []

    for article in raw_articles:
        link = article.get("link")
        if not link:
            continue

        # Si l'article est totalement inconnu
        if link not in queue_status:
            queue_status[link] = {
                "title": article.get("title"),
                "published": article.get("published"),
                "status": "pending"  # États possibles gérés : pending, processed, failed
            }
            new_articles.append(article)

    # Sauvegarde des modifications (les nouveaux articles passent en pending)
    save_queue_status(queue_status)
    
    print(f"File d'attente mise à jour : {len(new_articles)} nouveaux articles ajoutés en 'pending'.")
    return new_articles
