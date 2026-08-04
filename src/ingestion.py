import feedparser
from datetime import datetime
import pytz

ROME_TZ = pytz.timezone("Europe/Rome")

def fetch_rss_feed(feed_url):
    """
    Récupère et normalise les articles d'un flux RSS cible.
    """
    print(f"[Fantôme 1] Analyse du flux : {feed_url}")
    parsed_feed = feedparser.parse(feed_url)
    articles = []

    for entry in parsed_feed.entries:
        # Normalisation de la date de publication sur Europe/Rome
        pub_date = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            utc_date = datetime(*entry.published_parsed[:6], tzinfo=pytz.utc)
            pub_date = utc_date.astimezone(ROME_TZ).isoformat()
        else:
            pub_date = datetime.now(ROME_TZ).isoformat()

        article = {
            "id": entry.get("id", entry.get("link")),
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "summary": entry.get("summary", ""),
            "published": pub_date,
            "status": "pending"
        }
        articles.append(article)

    return articles
