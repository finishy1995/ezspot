import unittest
import mock

import src.libs.aws_client as client


class TestClient(unittest.TestCase):
    def test_profile(self):
        self.assertEqual(client.client({}), 1)
