import unittest
from unittest.mock import patch, MagicMock
from testfixtures import TempDirectory, LogCapture
from requests.exceptions import HTTPError

import os
import json

from hardware.CommunicationsPi.web_client import WebClient
from hardware.Utils.logger import Logger


class WebClientTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TempDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_init_no_log_no_server(self):
        with patch.dict(
            os.environ,
            {
                "WEB_CLIENT_LOG_FILE": "web_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            l_client = WebClient()

            self.assertTrue(l_client.logging is not None)
            self.assertTrue(l_client.logging.name == "WEB_CLIENT_LOG_FILE")
            self.assertIsInstance(l_client.logging, Logger)

            self.assertEqual(l_client.url, "https://0.0.0.0:0")

    def test_init_no_log_no_server_http(self):
        with patch.dict(
            os.environ,
            {
                "WEB_CLIENT_LOG_FILE": "web_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            l_client = WebClient()

            self.assertTrue(l_client.logging is not None)
            self.assertTrue(l_client.logging.name == "WEB_CLIENT_LOG_FILE")
            self.assertIsInstance(l_client.logging, Logger)

            self.assertEqual(l_client.url, "http://0.0.0.0:0")

    def test_init_no_log_server(self):
        with patch.dict(
            os.environ,
            {
                "WEB_CLIENT_LOG_FILE": "web_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            l_client = WebClient(server_url="/url")

            self.assertTrue(l_client.logging is not None)
            self.assertTrue(l_client.logging.name == "WEB_CLIENT_LOG_FILE")
            self.assertIsInstance(l_client.logging, Logger)

            self.assertEqual(l_client.url, "/url")

    def test_init_log_no_server(self):
        with patch.dict(
            os.environ,
            {
                "NEW_LOG_FILE": "web_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            l_client = WebClient(log_file_name="NEW_LOG_FILE")

            self.assertTrue(l_client.logging is not None)
            self.assertTrue(l_client.logging.name == "NEW_LOG_FILE")
            self.assertIsInstance(l_client.logging, Logger)

            self.assertEqual(l_client.url, "https://0.0.0.0:0")

    def test_init_log_server(self):
        with patch.dict(
            os.environ,
            {
                "NEW_LOG_FILE": "web_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            l_client = WebClient(log_file_name="NEW_LOG_FILE", server_url="/url")

            self.assertTrue(l_client.logging is not None)
            self.assertTrue(l_client.logging.name == "NEW_LOG_FILE")
            self.assertIsInstance(l_client.logging, Logger)

            self.assertEqual(l_client.url, "/url")

    @patch("hardware.CommunicationsPi.web_client.requests")
    def test_send_payload(self, mock_requests=MagicMock()):
        with patch.dict(
            os.environ,
            {
                "WEB_CLIENT_LOG_FILE": "web_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            with LogCapture() as capture:
                l_client = WebClient()

                payload = '{"key": "value" }'
                payload = json.loads(payload)

                l_client.send(payload)

                mock_requests.post.assert_called_with("https://0.0.0.0:0", json=payload)
                capture.check(
                    ("WEB_CLIENT_LOG_FILE", "INFO", "Pinging: https://0.0.0.0:0"),
                    ("WEB_CLIENT_LOG_FILE", "INFO", f"data: { payload }"),
                )

    @patch("hardware.CommunicationsPi.web_client.requests")
    def test_ping_server_raise_http_ex(self, mock_requests=MagicMock()):
        with patch.dict(
            os.environ,
            {
                "WEB_CLIENT_LOG_FILE": "web_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            with LogCapture() as capture:
                l_client = WebClient()
                mock_requests.post.side_effect = HTTPError("HTTPError")

                payload = '{"key": "value" }'
                payloadJson = json.loads(payload)

                with self.assertRaises(HTTPError):
                    l_client.send(payloadJson)

                mock_requests.post.assert_called_with(
                    "https://0.0.0.0:0", json=payloadJson
                )

                with self.assertRaises(HTTPError):
                    l_client.send(payload, is_json=False)

                mock_requests.post.assert_called_with("https://0.0.0.0:0", data=payload)

                capture.check(
                    ("WEB_CLIENT_LOG_FILE", "INFO", "Pinging: https://0.0.0.0:0"),
                    ("WEB_CLIENT_LOG_FILE", "INFO", f"data: { payloadJson }"),
                    ("WEB_CLIENT_LOG_FILE", "ERROR", "HTTP error occurred: HTTPError"),
                    ("WEB_CLIENT_LOG_FILE", "INFO", "Pinging: https://0.0.0.0:0"),
                    ("WEB_CLIENT_LOG_FILE", "INFO", f"data: { payload }"),
                    ("WEB_CLIENT_LOG_FILE", "ERROR", "HTTP error occurred: HTTPError"),
                )

    @patch("hardware.CommunicationsPi.web_client.requests")
    def test_ping_server_raise_ex(self, mock_requests=MagicMock()):
        with patch.dict(
            os.environ,
            {
                "WEB_CLIENT_LOG_FILE": "web_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            with LogCapture() as capture:
                l_client = WebClient()
                mock_requests.post.side_effect = Exception("Exception")

                payload = '{"key": "value" }'
                payload = json.loads(payload)

                with self.assertRaises(Exception):
                    l_client.send(payload)

                mock_requests.post.assert_called_with("https://0.0.0.0:0", json=payload)
                capture.check(
                    ("WEB_CLIENT_LOG_FILE", "INFO", "Pinging: https://0.0.0.0:0"),
                    ("WEB_CLIENT_LOG_FILE", "INFO", f"data: { payload }"),
                    ("WEB_CLIENT_LOG_FILE", "ERROR", "error occurred: Exception"),
                )


if __name__ == "__main__":
    unittest.main()
