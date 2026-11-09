import unittest
from unittest.mock import Mock, patch
import scraper

class PublicProfileSearchTests(unittest.TestCase):
    @patch.dict("os.environ", {"SERPAPI_API_KEY":"test-key"})
    @patch("scraper.requests.get")
    def test_keeps_only_public_linkedin_profile_urls(self, get):
        response=Mock()
        response.raise_for_status.return_value=None
        response.json.return_value={"organic_results":[
            {"title":"A. Analyst - LinkedIn","snippet":"Data analyst","link":"https://www.linkedin.com/in/a-analyst/?trk=search"},
            {"title":"Company page","snippet":"Company","link":"https://www.linkedin.com/company/example"},
            {"title":"External result","snippet":"Other","link":"https://example.com/profile"}
        ]}
        get.return_value=response
        rows=scraper.search_public_profiles("Data Analyst","India",limit=10)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["profile_url"],"https://www.linkedin.com/in/a-analyst/")
        self.assertEqual(rows[0]["source"],"Google public search result")
        get.assert_called_once()

    @patch.dict("os.environ", {}, clear=True)
    def test_missing_api_key_fails_clearly(self):
        with self.assertRaisesRegex(RuntimeError,"SERPAPI_API_KEY"):
            scraper.search_public_profiles("Data Analyst","India")

if __name__=="__main__":
    unittest.main()
