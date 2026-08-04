from src.ingestion import fetch_rss_feed
from src.processor import filter_new_articles

# Exemple de flux RSS cible (tu pourras remplacer l'URL par la suite)
SAMPLE_RSS_URL = "https://www.ansa.it/sito/notizie/sport/calcio/calcio_rss.xml"

def run_pipeline():
    print("--- Démarrage du pipeline Gioiello Vitale ---")

    # 1. Récupération des articles via le Fantôme 1
    raw_articles = fetch_rss_feed(SAMPLE_RSS_URL)
    print(f"Articles bruts récupérés : {len(raw_articles)}")

    # 2. Filtrage pour ne garder que les nouveautés (idempotence)
    new_articles = filter_new_articles(raw_articles)
    print(f"Nouveaux articles après filtrage : {len(new_articles)}")

    for art in new_articles:
        print(f" -> [Inédit] {art['title']}")

if __name__ == "__main__":
    run_pipeline()
