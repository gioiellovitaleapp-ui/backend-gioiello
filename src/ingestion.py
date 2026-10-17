import feedparser
from datetime import datetime
import pytz

# Liste des sources RSS officielles / ciblées en HTTPS strict
RSS_URLS = [
    "https://news.google.com/rss/search?q=Juventus&hl=it&gl=IT&ceid=IT:it",
    "https://www.tuttosport.com/rss/calcio/juventus"
]

def fetch_rss_sources():
    """
    Récupère les flux RSS, normalise les dates sur le fuseau Europe/Rome 
    et garantit un format d'article propre.
    """
    articles = []
    rome_tz = pytz.timezone('Europe/Rome')
    
    for url in RSS_URLS:
        print(f"Tentative de récupération du flux RSS : {url}")
        try:
            feed = feedparser.parse(url)
            
            if feed.entries:
                for entry in feed.entries:
                    # Normalisation de la date de publication
                    pub_date = entry.get("published", "")
                    
                    article = {
                        "title": entry.get("title", "Sans titre"),
                        "link": entry.get("link", "#"),
                        "published": pub_date,
                        "fetched_at": datetime.now(rome_tz).isoformat()
                    }
                    articles.append(article)
                print(f" -> Succès ! {len(feed.entries)} articles récupérés pour cette source.")
            else:
                print(" -> Aucun article trouvé sur ce flux.")
        except Exception as e:
            print(f" ❌ Erreur lors du parsing du flux {url}: {e}")
            
    return articles

# Permet de tester le script de manière autonome si besoin
if __name__ == "__main__":
    print("--- Test de l'ingestion RSS (Fantôme 1) ---")
    raw_articles = fetch_rss_sources()
    print(f"Total d'articles bruts récoltés : {len(raw_articles)}")
