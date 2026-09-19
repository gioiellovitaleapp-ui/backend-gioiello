import json
import os

STATUS_FILE = "queue_status.json"
OUTPUT_FILE = "feed_output.json"

def export_feed_for_frontend():
    """
    Extrait les articles de la file d'attente et génère un fichier JSON 
    épuré pour l'affichage dans le Pôle 2 (Mercato & Actualités).
    """
    if not os.path.exists(STATUS_FILE):
        print("Aucun fichier de file d'attente trouvé.")
        return

    with open(STATUS_FILE, "r", encoding="utf-8") as f:
        queue_data = json.load(f)

    feed_items = []
    
    # On parcourt les articles pour ne garder que ceux qui sont exploitables
    for link, data in queue_data.items():
        # On inclut les 'pending' ou 'processed' (selon la logique d'affichage)
        if data.get("status") in ["pending", "processed"]:
            feed_items.append({
                "title": data.get("title"),
                "link": link,
                "published": data.get("published"),
                "status": data.get("status")
            })

    # Tri par date de publication (du plus récent au plus ancien si disponible)
    # Sauvegarde dans le fichier final pour le front-end
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(feed_items, f, ensure_ascii=False, indent=4)

    print(f"Export réussi : {len(feed_items)} articles écrits dans {OUTPUT_FILE}.")

if __name__ == "__main__":
    export_feed_for_frontend()
