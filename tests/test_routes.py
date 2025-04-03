import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
import json
from app.routes.article import register_routes

class TestArticleRoutes(unittest.TestCase):
    def setUp(self):
        """
        Set up test client and application for each test.
        """
        self.app = Flask(__name__)
        register_routes(self.app)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """
        Clean up after each test.
        """
        self.app_context.pop()

    @patch('app.service.article.ArticleService.get_all_articles')
    def test_get_articles(self, mock_get_all_articles):
        """
        Test the GET /api/articles endpoint.
        """
        mock_paginated = MagicMock()
        mock_paginated.items = [
            {'id': 1, 'url': 'http://example.com/article1'},
            {'id': 2, 'url': 'http://example.com/article2'}
        ]
        mock_paginated.page = 1
        mock_paginated.per_page = 20
        mock_paginated.pages = 1
        mock_paginated.total = 2
        
        mock_get_all_articles.return_value = mock_paginated
        
        response = self.client.get('/api/articles')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        
        self.assertIn('articles', data)
        self.assertIn('pagination', data)
        self.assertEqual(len(data['articles']), 2)
        self.assertEqual(data['pagination']['page'], 1)
        self.assertEqual(data['pagination']['total_items'], 2)
        
        mock_get_all_articles.assert_called_once_with(1, 20)

    @patch('app.service.article.ArticleService.get_latest_articles')
    def test_get_latest_articles(self, mock_get_latest_articles):
        """
        Test the GET /api/articles/latest endpoint.
        """
        mock_paginated = MagicMock()
        mock_paginated.items = [
            {'id': 1, 'url': 'http://example.com/article1', 'latest_version': {'version': 1, 'content': 'Content 1'}},
            {'id': 2, 'url': 'http://example.com/article2', 'latest_version': {'version': 1, 'content': 'Content 2'}}
        ]
        mock_paginated.page = 1
        mock_paginated.per_page = 20
        mock_paginated.pages = 1
        mock_paginated.total = 2
        
        mock_get_latest_articles.return_value = mock_paginated
        
        response = self.client.get('/api/articles/latest')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        
        self.assertIn('articles', data)
        self.assertIn('pagination', data)
        self.assertEqual(len(data['articles']), 2)
        self.assertEqual(data['pagination']['page'], 1)
        self.assertEqual(data['pagination']['total_items'], 2)
        
        mock_get_latest_articles.assert_called_once_with(1, 20)

    @patch('app.service.article.ArticleService.get_article_by_id')
    def test_get_article(self, mock_get_article_by_id):
        """
        Test the GET /api/articles/<id> endpoint.
        """
        mock_article = {'id': 1, 'url': 'http://example.com/article1'}
        
        mock_get_article_by_id.return_value = mock_article
        
        response = self.client.get('/api/articles/1')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['url'], 'http://example.com/article1')
        
        mock_get_article_by_id.assert_called_once_with(1)

    @patch('app.service.article.ArticleService.get_article_versions')
    def test_get_article_versions(self, mock_get_article_versions):
        """
        Test the GET /api/articles/<id>/versions endpoint.
        """
        mock_paginated = MagicMock()
        mock_paginated.items = [
            {'article_id': 1, 'version': 1, 'content': 'Content v1'},
            {'article_id': 1, 'version': 2, 'content': 'Content v2'}
        ]
        mock_paginated.page = 1
        mock_paginated.per_page = 10
        mock_paginated.pages = 1
        mock_paginated.total = 2
        
        mock_get_article_versions.return_value = mock_paginated
        
        response = self.client.get('/api/articles/1/versions')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        
        self.assertEqual(data['article_id'], 1)
        self.assertIn('versions', data)
        self.assertIn('pagination', data)
        self.assertEqual(len(data['versions']), 2)
        self.assertEqual(data['pagination']['page'], 1)
        self.assertEqual(data['pagination']['total_items'], 2)
        
        mock_get_article_versions.assert_called_once_with(1, 1, 10)

    @patch('app.routes.article.Crawler')
    def test_run_crawler(self, MockCrawler):
        """
        Test the POST /api/crawler/run endpoint.
        """
        mock_crawler_instance = MagicMock()
        mock_crawler_instance.crawl_overview_page.return_value = [
            'http://example.com/article1',
            'http://example.com/article2'
        ]
        MockCrawler.return_value = mock_crawler_instance
        
        response = self.client.post('/api/crawler/run')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], f'Crawler job completed. Processed 2 article URLs.')
        
        MockCrawler.assert_called_once()
        mock_crawler_instance.crawl_overview_page.assert_called_once()

    def test_pagination_parameters(self):
        """
        Test that pagination parameters are correctly parsed.
        """
        with patch('app.service.article.ArticleService.get_all_articles') as mock_get_all:
            mock_paginated = MagicMock()
            mock_paginated.items = []
            mock_paginated.page = 2
            mock_paginated.per_page = 15
            mock_paginated.pages = 5
            mock_paginated.total = 75
            
            mock_get_all.return_value = mock_paginated
            
            response = self.client.get('/api/articles?page=2&per_page=15')
            
            mock_get_all.assert_called_once_with(2, 15)
            
            data = json.loads(response.data)
            self.assertEqual(data['pagination']['page'], 2)
            self.assertEqual(data['pagination']['per_page'], 15)


if __name__ == '__main__':
    unittest.main()