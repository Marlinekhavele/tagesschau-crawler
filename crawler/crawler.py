import re
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from app.service.article import ArticleService
from config import Config

logger = logging.getLogger(__name__)


class Crawler:
    def __init__(self, base_url=None, overview_url=None):
        """
        Initialize the crawler with URLs.
        
        Args:
            base_url: Base URL for the site. If None, gets from Config.
            overview_url: URL for the overview page. If None, gets from Config.
        """
        # Initialize URLs from parameters or Config directly
        self.base_url = base_url or Config.TAGESSCHAU_BASE_URL
        self.overview_url = overview_url or Config.TAGESSCHAU_OVERVIEW_URL
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        logger.info(f"Crawler initialized with base_url: {self.base_url}, overview_url: {self.overview_url}")

    def crawl_overview_page(self):
        """Crawl the overview page and extract article URLs"""
        logger.info(f"Crawling overview page: {self.overview_url}")

        try:
            response = requests.get(self.overview_url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all article links
            article_links = []

            # Look for article teasers
            teasers = soup.select('article.teaser, div.teaser')
            logger.info(f"Found {len(teasers)} teasers on the overview page")

            for teaser in teasers:
                # Find headline links
                links = teaser.select('a')

                for link in links:
                    href = link.get('href')
                    if href and self._is_valid_article_url(href):
                        full_url = urljoin(self.base_url, href)
                        if full_url not in article_links:
                            article_links.append(full_url)

            logger.info(f"Found {len(article_links)} article links")

            # Crawl each article page
            for url in article_links:
                self.crawl_article_page(url)

            return article_links

        except Exception as e:
            logger.error(f"Error crawling overview page: {str(e)}")
            return []

    def crawl_article_page(self, url):
        """
        Crawl an individual article page and extract content
        """
        logger.info(f"Crawling article page: {url}")

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract headline
            headline_element = soup.select_one('h1, .headline')
            headline = headline_element.get_text().strip() if headline_element else "No headline found"

            # Extract subheadline
            subheadline_element = soup.select_one('.dachzeile, .subtitle, .summary')
            subheadline = subheadline_element.get_text().strip() if subheadline_element else None

            # Extract content
            content_elements = soup.select('.content, .article-content, .text, article p')
            content = '\n\n'.join([elem.get_text().strip() for elem in content_elements if elem.get_text().strip()])

            # Extract date information
            date_element = soup.select_one('.date, .meta time, .timestamp')
            last_updated_at = None

            if date_element:
                date_text = date_element.get_text().strip()
                # Try different date formats - actual format needs to be adjusted
                try:
                    # Example pattern: "Stand: 01.04.2023 15:30 Uhr"
                    date_match = re.search(r'(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2})', date_text)
                    if date_match:
                        date_str = f"{date_match.group(1)} {date_match.group(2)}"
                        last_updated_at = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
                except Exception as e:
                    logger.warning(f"Could not parse date: {date_text}. Error: {str(e)}")

            # Store in database
            article, version, is_new_article, is_new_version = ArticleService.create_or_update_article(
                url=url,
                headline=headline,
                subheadline=subheadline,
                content=content,
                last_updated_at=last_updated_at
            )

            if is_new_article:
                logger.info(f"Created new article: {url}")

            if is_new_version:
                logger.info(f"Created new version for article: {url}")
            else:
                logger.info(f"No changes detected for article: {url}")

            return {
                'url': url,
                'headline': headline,
                'subheadline': subheadline,
                'content_length': len(content),
                'last_updated_at': last_updated_at,
                'is_new_article': is_new_article,
                'is_new_version': is_new_version
            }

        except Exception as e:
            logger.error(f"Error crawling article page {url}: {str(e)}")
            return None

    def _is_valid_article_url(self, url):
        """
        Check if URL is a valid article URL
        """
        if url.startswith('/'):
            url = urljoin(self.base_url, url)

        # Skip URLs that clearly aren't articles
        skip_patterns = [
            'facebook.com', 'twitter.com', 'instagram.com',
            '/impressum/', '/datenschutz/', '/kontakt/',
            '/suche/', '/login/', '/hilfe/'
        ]

        for pattern in skip_patterns:
            if pattern in url:
                return False

        # Include only typical article paths
        include_patterns = [
            '/news/', '/inland/', '/ausland/', '/wirtschaft/',
            '/regional/', '/sport/', '/politik/'
        ]

        for pattern in include_patterns:
            if pattern in url:
                return True

        return False