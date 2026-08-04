import feedparser
from src.processor import filter_new_articles

# Liste de tes sources RSS (la première qui répond fournit les articles)
RSS_URLS = [
    "https://news.google.com/rss/search?q=Juventus&hl=it&gl=IT&ceid=IT:it",
    "https://www.tuttosport.com/rss/calcio/juventus"
]

def fetch_rss_articles():
    articles = []
    for url in RSS_URLS:
        print(f"Tentative de récupération du flux RSS : {url}")
        feed = feedparser.parse(url)
        
        if feed.entries:
            for entry in feed.entries:
                article = {
                    "title": entry.get("title"),
                    "link": entry.get("link"),
                    "published": entry.get("published", "")
                }
                articles.append(article)
            print(f"Succès ! {len(articles)} articles trouvés avec cette source.")
            break # On s'arrête dès qu'une source fonctionne
        else:
            print("Aucun article trouvé sur ce flux, essai du suivant...")
            
    return articles
