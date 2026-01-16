from __future__ import annotations

import argparse
from datetime import datetime
try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

try:
    import feedparser
except ImportError:
    print("Error: feedparser is not installed.")
    print("Please install it using: pip install feedparser")
    import sys
    sys.exit(1)


class Article(TypedDict):
    title: str
    link: str
    published: str
    summary: str


def parse_rss_feed(feed_url: str) -> list[Article]:
    """Parse an RSS feed and extract article information.
    
    Args:
        feed_url: URL of the RSS feed to parse
        
    Returns:
        List of articles with title, link, published date, and summary
    """
    feed = feedparser.parse(feed_url)
    
    # Check for feed errors
    if hasattr(feed, 'bozo') and feed.bozo:
        if hasattr(feed, 'bozo_exception'):
            raise Exception(f"Feed parsing error: {feed.bozo_exception}")
    
    articles: list[Article] = []
    
    for entry in feed.entries:
        # Extract published date, fallback to current date if not available
        published = entry.get("published", "")
        if not published and hasattr(entry, "published_parsed") and entry.published_parsed:
            try:
                published = datetime(*entry.published_parsed[:6]).isoformat()
            except (TypeError, ValueError):
                published = datetime.now().isoformat()
        if not published:
            published = datetime.now().isoformat()
        
        # Extract summary, fallback to description or empty string
        summary = entry.get("summary", entry.get("description", ""))
        
        article: Article = {
            "title": entry.get("title", "No title"),
            "link": entry.get("link", ""),
            "published": published,
            "summary": summary,
        }
        articles.append(article)
    
    return articles


def format_article(article: Article, index: int) -> str:
    """Format an article for display.
    
    Args:
        article: Article dictionary with title, link, published, and summary
        index: Article number for display
        
    Returns:
        Formatted string representation of the article
    """
    lines = [
        f"\n{'=' * 80}",
        f"Article #{index}",
        f"{'=' * 80}",
        f"Title: {article['title']}",
        f"Link: {article['link']}",
        f"Published: {article['published']}",
        f"\nSummary:",
        article['summary'],
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse daily news articles from RSS feeds and extract summaries"
    )
    parser.add_argument(
        "feed_urls",
        nargs="+",
        help="One or more RSS feed URLs to parse",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of articles to display per feed (default: 10)",
    )
    
    args = parser.parse_args()
    
    for feed_url in args.feed_urls:
        print(f"\n{'#' * 80}")
        print(f"Fetching articles from: {feed_url}")
        print(f"{'#' * 80}")
        
        try:
            articles = parse_rss_feed(feed_url)
            
            if not articles:
                print("No articles found in this feed.")
                continue
            
            # Limit the number of articles to display
            articles_to_show = articles[:args.limit]
            
            for idx, article in enumerate(articles_to_show, start=1):
                print(format_article(article, idx))
            
            if len(articles) > args.limit:
                print(f"\n... and {len(articles) - args.limit} more articles")
                
        except Exception as exc:
            print(f"Error parsing feed {feed_url}: {exc}")


if __name__ == "__main__":
    main()
