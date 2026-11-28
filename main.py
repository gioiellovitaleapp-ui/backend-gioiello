import json
import feedparser
from src.processor import filter_new_articles

# Liste des sources RSS
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
            print(f"Succès ! Articles récupérés pour cette source.")
        else:
            print("Aucun article trouvé sur ce flux, essai du suivant...")
            
    return articles

if __name__ == "__main__":
    print("--- Lancement du Pipeline Gioiello Vitale ---")
    raw_articles = fetch_rss_articles()
    print(f"Articles bruts trouvés au total : {len(raw_articles)}")
    
    # Passage par le filtre d'idempotence
    new_articles = filter_new_articles(raw_articles)
    print(f"Nouveaux articles après filtrage : {len(new_articles)}")
    
    # Sauvegarde des résultats dans feed_output.json à la racine
    output_filename = "feed_output.json"
    print(f"Écriture des données dans {output_filename}...")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(new_articles, f, ensure_ascii=False, indent=4)
    print("Exportation terminée avec succès.")
