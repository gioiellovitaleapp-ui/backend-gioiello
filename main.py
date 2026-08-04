import feedparser
from src.processor import filter_new_articles

# URL de ton flux RSS (tu pourras remplacer par ton flux cible)
RSS_URL = "https://www.gazzetta.it/rss/squadra/juventus.xml" 

def fetch_rss_articles():
    print(f"Récupération du flux RSS : {RSS_URL}")
    feed = feedparser.parse(RSS_URL)
    articles = []
    
    for entry in feed.entries:
        article = {
            "title": entry.get("title"),
            "link": entry.get("link"),
            "published": entry.get("published", "")
        }
        articles.append(article)
        
    print(f"Articles bruts trouvés dans le flux : {len(articles)}")
    return articles

def main():
    print("--- Lancement du Pipeline Gioiello Vitale ---")
    
    # 1. Récupération des articles bruts du flux RSS
    articles_bruts = fetch_rss_articles()
    
    if not articles_bruts:
        print("Aucun article trouvé dans le flux.")
        return

    # 2. Application de la Forteresse Idempotente (via src/processor.py)
    # Cela met à jour 'queue_status.json' et isole uniquement les nouveautés
    articles_a_traiter = filter_new_articles(articles_bruts)
    
    print(f"Articles réellement en attente de traitement (pending) : {len(articles_a_traiter)}")
    
    for art in articles_a_traiter:
        print(f" - [NOUVEAU] {art['title']}")

    print("--- Fin du traitement du pipeline ---")

if __name__ == "__main__":
    main()
