import unittest
import logging
import requests

unittest.TestLoader.sortTestMethodsUsing = None


class TestAPIKeyHandler(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestAPIKeyHandler, self).__init__(*args, **kwargs)

    def test_server(self):
        """Test server"""
        result = requests.get(url="http://localhost:5000/")
        result = result.json()
        self.assertEqual(
            result["message"], "API Key Generator Assignment from Codeuino for LF Mentorship")

    def test_gen_api(self):
        """Test generate api key"""
        result = requests.post(url="http://localhost:5000/key")
        result = result.json()
        self.assertEqual(
            result["message"], "Generated")

    def test_get_api(self):
        """Test get an available api key"""
        result = requests.get(url="http://localhost:5000/key")
        result = result.json()
        self.assertEqual(
            result["message"], "Success")

    def test_del_api(self):
        """Test delete api key"""
        # generate API key
        requests.post(url="http://localhost:5000/key")

        # Get the API key
        result = requests.get(url="http://localhost:5000/key")
        result = result.json()
        api_key = result["key"]
        url = "http://localhost:5000/key/del/"
        api_url = url + api_key
        result = requests.delete(url=api_url)
        result = result.json()
        self.assertEqual(
            result["message"], "Success")

    def test_unblock_api(self):
        """Test unblock an api key"""
        # generate API key
        requests.post(url="http://localhost:5000/key")

        # Get the API key
        result = requests.get(url="http://localhost:5000/key")
        result = result.json()
        api_key = result["key"]

        url = "http://localhost:5000/key/unblock/"
        api_url = url + api_key
        result = requests.post(url=api_url)
        result = result.json()
        self.assertEqual(
            result["message"], "Success")

    def test_poll_api(self):
        """Test poll for extending expiration of an api key"""
        # generate API key
        requests.post(url="http://localhost:5000/key")

        # Get the API key
        result = requests.get(url="http://localhost:5000/key")
        result = result.json()
        api_key = result["key"]

        url = "http://localhost:5000/key/poll/"
        api_url = url + api_key
        result = requests.post(url=api_url)
        result = result.json()
        self.assertEqual(
            result["message"], "Success")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestAPIKeyHandler").setLevel(logging.ERROR)
    unittest.main()
