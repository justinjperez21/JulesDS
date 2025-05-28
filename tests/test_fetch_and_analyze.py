import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os

# Add project root to sys.path to allow importing from scripts
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from scripts.fetch_and_analyze import fetch_news_titles

class TestFetchNewsTitles(unittest.TestCase):

    @patch('scripts.fetch_and_analyze.GoogleNews')
    def test_fetch_news_successful_parsing(self, MockGoogleNews):
        # Configure the mock
        mock_gn_instance = MockGoogleNews.return_value
        sample_mock_data = [
            {'title': 'Test Article 1', 'published': 'Wed, 29 May 2024 10:00:00 GMT'},
            {'title': 'Test Article 2', 'published': 'Thu, 30 May 2024 12:30:00 GMT'}
        ]
        mock_gn_instance.search.return_value = {'entries': sample_mock_data}

        # Call the function
        articles = fetch_news_titles(target_count=len(sample_mock_data))

        # Assertions
        self.assertEqual(len(articles), 2)
        
        self.assertIsInstance(articles[0], dict)
        self.assertEqual(articles[0]['title'], 'Test Article 1')
        self.assertIsInstance(articles[0]['date'], datetime)
        self.assertEqual(articles[0]['date'], datetime(2024, 5, 29, 10, 0, 0))

        self.assertIsInstance(articles[1], dict)
        self.assertEqual(articles[1]['title'], 'Test Article 2')
        self.assertIsInstance(articles[1]['date'], datetime)
        self.assertEqual(articles[1]['date'], datetime(2024, 5, 30, 12, 30, 0))
        
        mock_gn_instance.search.assert_called_once_with('world news', when='7d')

    @patch('scripts.fetch_and_analyze.GoogleNews')
    def test_fetch_news_api_failure(self, MockGoogleNews):
        # Configure the mock to raise an exception
        mock_gn_instance = MockGoogleNews.return_value
        mock_gn_instance.search.side_effect = Exception("API Error")

        # Call the function
        articles = fetch_news_titles()

        # Assertions
        self.assertEqual(len(articles), 0)
        mock_gn_instance.search.assert_called_once_with('world news', when='7d')

    @patch('scripts.fetch_and_analyze.GoogleNews')
    def test_fetch_news_no_entries_returned(self, MockGoogleNews):
        # Configure the mock to return no entries
        mock_gn_instance = MockGoogleNews.return_value
        mock_gn_instance.search.return_value = {'entries': []}

        # Call the function
        articles = fetch_news_titles()

        # Assertions
        self.assertEqual(len(articles), 0)
        mock_gn_instance.search.assert_called_once_with('world news', when='7d')

    @patch('scripts.fetch_and_analyze.GoogleNews')
    def test_fetch_news_search_returns_none(self, MockGoogleNews):
        # Configure the mock to return None from search
        mock_gn_instance = MockGoogleNews.return_value
        mock_gn_instance.search.return_value = None

        # Call the function
        articles = fetch_news_titles()

        # Assertions
        self.assertEqual(len(articles), 0)
        mock_gn_instance.search.assert_called_once_with('world news', when='7d')

    @patch('scripts.fetch_and_analyze.GoogleNews')
    def test_fetch_news_search_returns_dict_without_entries(self, MockGoogleNews):
        # Configure the mock to return a dict without 'entries' key
        mock_gn_instance = MockGoogleNews.return_value
        mock_gn_instance.search.return_value = {} # No 'entries' key

        # Call the function
        articles = fetch_news_titles()

        # Assertions
        self.assertEqual(len(articles), 0)
        mock_gn_instance.search.assert_called_once_with('world news', when='7d')

    @patch('scripts.fetch_and_analyze.GoogleNews')
    def test_fetch_news_malformed_date(self, MockGoogleNews):
        # Configure the mock
        mock_gn_instance = MockGoogleNews.return_value
        sample_mock_data = [
            {'title': 'Test Article Valid Date', 'published': 'Fri, 31 May 2024 10:00:00 GMT'},
            {'title': 'Test Article Malformed Date', 'published': 'Invalid Date String'},
            {'title': 'Test Article Another Valid', 'published': 'Sat, 01 Jun 2024 12:00:00 GMT'}
        ]
        mock_gn_instance.search.return_value = {'entries': sample_mock_data}

        # Call the function
        articles = fetch_news_titles(target_count=len(sample_mock_data))

        # Assertions
        self.assertEqual(len(articles), 2) # Only valid dates should be parsed
        self.assertEqual(articles[0]['title'], 'Test Article Valid Date')
        self.assertEqual(articles[0]['date'], datetime(2024, 5, 31, 10, 0, 0))
        self.assertEqual(articles[1]['title'], 'Test Article Another Valid')
        self.assertEqual(articles[1]['date'], datetime(2024, 6, 1, 12, 0, 0))

    @patch('scripts.fetch_and_analyze.GoogleNews')
    def test_fetch_news_missing_title_or_date(self, MockGoogleNews):
        # Configure the mock
        mock_gn_instance = MockGoogleNews.return_value
        sample_mock_data = [
            {'published': 'Mon, 03 Jun 2024 10:00:00 GMT'}, # Missing title
            {'title': 'Test Article Only Title'}, # Missing published date
            {'title': 'Test Article Complete', 'published': 'Tue, 04 Jun 2024 12:00:00 GMT'},
            {'title': None, 'published': 'Wed, 05 Jun 2024 10:00:00 GMT'}, # Title is None
            {'title': 'Test Article Date None', 'published': None} # Date is None
        ]
        mock_gn_instance.search.return_value = {'entries': sample_mock_data}

        # Call the function
        articles = fetch_news_titles(target_count=len(sample_mock_data))

        # Assertions
        self.assertEqual(len(articles), 1) # Only one complete article
        self.assertEqual(articles[0]['title'], 'Test Article Complete')
        self.assertEqual(articles[0]['date'], datetime(2024, 6, 4, 12, 0, 0))
    
    @patch('scripts.fetch_and_analyze.GoogleNews')
    def test_target_count_respected(self, MockGoogleNews):
        mock_gn_instance = MockGoogleNews.return_value
        sample_mock_data = [
            {'title': f'Article {i}', 'published': 'Wed, 29 May 2024 10:00:00 GMT'} for i in range(5)
        ]
        mock_gn_instance.search.return_value = {'entries': sample_mock_data}

        articles = fetch_news_titles(target_count=2)
        self.assertEqual(len(articles), 2)

        articles = fetch_news_titles(target_count=5)
        self.assertEqual(len(articles), 5)

        # Test with target_count > available articles
        articles = fetch_news_titles(target_count=10) 
        self.assertEqual(len(articles), 5)


if __name__ == '__main__':
    unittest.main()
