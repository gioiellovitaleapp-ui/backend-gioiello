import json
import os

STATUS_FILE = "queue_status.json"

def load_queue_status():
    """Charge l'état de la file d'attente depuis le fichier JSON."""
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_queue_status(status_data):
    """Sauvegarde l'état de la file d'attente."""
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status_data, f, ensure_ascii=False, indent=2)

def filter_new_articles(articles):
    """
    Filtre les articles pour ne garder que les nouveautés,
    met à jour le fichier d'état et protège les quotas.
    """
    status_data = load_queue_status()
    new_articles = []

    for article in articles:
        # On récupère le lien unique de l'article (clé d'identification)
        link = article.get("link")
        if not link:
            continue
            
        # Si l'article a déjà été traité avec succès, on l'ignore
        if status_data.get(link) == "processed":
            continue
            
        # Sinon, c'est un nouvel article : on le marque comme 'pending'
        status_data[link] = "pending"
        new_articles.append(article)

    # On sauvegarde l'état mis à jour dans le fichier JSON
    save_queue_status(status_data)
    return new_articles
