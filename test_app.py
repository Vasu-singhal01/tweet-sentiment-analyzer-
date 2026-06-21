import io
import os
import unittest
from unittest.mock import patch

from app import app, fetch_xquik_tweets, tweets_for_keyword


class XquikTweetSourceTest(unittest.TestCase):
    def test_fetch_xquik_tweets_maps_text_fields(self):
        class Response(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, traceback):
                return False

        payload = (
            b'{"tweets":[{"text":"First tweet"},{"fullText":"Second tweet"},'
            b'{"full_text":"Third tweet"},{"id":"missing text"}]}'
        )
        seen_urls = []

        def fake_urlopen(request, timeout):
            seen_urls.append(request.full_url)
            self.assertEqual(timeout, 8)
            return Response(payload)

        with patch.dict(
            os.environ,
            {
                "XQUIK_API_KEY": "test-key",
                "XQUIK_SEARCH_URL": "https://xquik.test/search",
            },
        ):
            with patch("app.urlopen", fake_urlopen):
                tweets = fetch_xquik_tweets("python", limit=2)

        self.assertEqual(
            tweets,
            [
                {"text": "First tweet", "category": "live"},
                {"text": "Second tweet", "category": "live"},
                {"text": "Third tweet", "category": "live"},
            ],
        )
        self.assertIn("q=python", seen_urls[0])
        self.assertIn("limit=2", seen_urls[0])

    def test_tweets_for_keyword_falls_back_without_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "app.generate_tweets",
                return_value=[{"text": "sample tweet", "category": "positive"}],
            ):
                tweets, source = tweets_for_keyword("python")

        self.assertEqual(source, "sample")
        self.assertEqual(tweets, [{"text": "sample tweet", "category": "positive"}])

    def test_analyze_uses_live_tweets_when_available(self):
        with patch(
            "app.fetch_xquik_tweets",
            return_value=[{"text": "I love Python", "category": "live"}],
        ):
            response = app.test_client().post("/analyze", json={"keyword": "python"})

        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body["source"], "xquik")
        self.assertEqual(body["total"], 1)
        self.assertEqual(body["tweets"][0]["text"], "I love Python")


if __name__ == "__main__":
    unittest.main()
