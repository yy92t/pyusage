import unittest
from datetime import datetime
from unittest.mock import Mock, patch

import rss_news_parser


class TestRSSNewsParser(unittest.TestCase):
    def test_parse_rss_feed_basic(self):
        """Test parsing a basic RSS feed with standard fields."""
        mock_feed = Mock()
        mock_entry = Mock()
        mock_entry.get = lambda key, default="": {
            "title": "Test Article",
            "link": "https://example.com/article",
            "published": "2026-01-13T10:00:00",
            "summary": "This is a test summary",
        }.get(key, default)
        mock_entry.title = "Test Article"
        mock_entry.link = "https://example.com/article"
        mock_entry.published = "2026-01-13T10:00:00"
        mock_entry.summary = "This is a test summary"
        
        mock_feed.entries = [mock_entry]
        
        with patch("rss_news_parser.feedparser.parse", return_value=mock_feed):
            articles = rss_news_parser.parse_rss_feed("https://example.com/feed")
        
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["title"], "Test Article")
        self.assertEqual(articles[0]["link"], "https://example.com/article")
        self.assertEqual(articles[0]["published"], "2026-01-13T10:00:00")
        self.assertEqual(articles[0]["summary"], "This is a test summary")
    
    def test_parse_rss_feed_empty(self):
        """Test parsing an empty RSS feed."""
        mock_feed = Mock()
        mock_feed.entries = []
        
        with patch("rss_news_parser.feedparser.parse", return_value=mock_feed):
            articles = rss_news_parser.parse_rss_feed("https://example.com/feed")
        
        self.assertEqual(len(articles), 0)
    
    def test_parse_rss_feed_missing_fields(self):
        """Test parsing RSS feed entries with missing fields."""
        mock_feed = Mock()
        mock_entry = Mock()
        mock_entry.get = lambda key, default="": {"title": "Minimal Article"}.get(key, default)
        mock_entry.title = "Minimal Article"
        
        # hasattr should return False for published_parsed
        type(mock_entry).published_parsed = property(lambda self: None)
        
        mock_feed.entries = [mock_entry]
        
        with patch("rss_news_parser.feedparser.parse", return_value=mock_feed):
            articles = rss_news_parser.parse_rss_feed("https://example.com/feed")
        
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["title"], "Minimal Article")
        self.assertEqual(articles[0]["link"], "")
        self.assertEqual(articles[0]["summary"], "")
        # Published should be set to current time
        self.assertTrue(len(articles[0]["published"]) > 0)
    
    def test_parse_rss_feed_with_description_fallback(self):
        """Test that description is used when summary is not available."""
        mock_feed = Mock()
        mock_entry = Mock()
        mock_entry.get = lambda key, default="": {
            "title": "Test Article",
            "description": "This is the description",
        }.get(key, default)
        mock_entry.title = "Test Article"
        mock_entry.description = "This is the description"
        
        # hasattr should return False for published_parsed
        type(mock_entry).published_parsed = property(lambda self: None)
        
        mock_feed.entries = [mock_entry]
        
        with patch("rss_news_parser.feedparser.parse", return_value=mock_feed):
            articles = rss_news_parser.parse_rss_feed("https://example.com/feed")
        
        self.assertEqual(articles[0]["summary"], "This is the description")
    
    def test_format_article(self):
        """Test formatting an article for display."""
        article = rss_news_parser.Article(
            title="Test Title",
            link="https://example.com/article",
            published="2026-01-13T10:00:00",
            summary="Test summary content",
        )
        
        formatted = rss_news_parser.format_article(article, 1)
        
        self.assertIn("Article #1", formatted)
        self.assertIn("Test Title", formatted)
        self.assertIn("https://example.com/article", formatted)
        self.assertIn("2026-01-13T10:00:00", formatted)
        self.assertIn("Test summary content", formatted)
    
    def test_parse_rss_feed_multiple_entries(self):
        """Test parsing RSS feed with multiple entries."""
        mock_feed = Mock()
        
        entries = []
        for i in range(5):
            mock_entry = Mock()
            mock_entry.get = lambda key, default="", idx=i: {
                "title": f"Article {idx}",
                "link": f"https://example.com/article{idx}",
                "published": f"2026-01-13T{10+idx}:00:00",
                "summary": f"Summary {idx}",
            }.get(key, default)
            mock_entry.title = f"Article {i}"
            mock_entry.link = f"https://example.com/article{i}"
            mock_entry.published = f"2026-01-13T{10+i}:00:00"
            mock_entry.summary = f"Summary {i}"
            entries.append(mock_entry)
        
        mock_feed.entries = entries
        
        with patch("rss_news_parser.feedparser.parse", return_value=mock_feed):
            articles = rss_news_parser.parse_rss_feed("https://example.com/feed")
        
        self.assertEqual(len(articles), 5)
        for i, article in enumerate(articles):
            self.assertEqual(article["title"], f"Article {i}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
