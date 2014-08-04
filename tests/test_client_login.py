import sys
import unittest
import json
import httplib2
from urllib import urlencode

from test_base import BaseTestCase


class LoginTestCase(BaseTestCase):
    def test_login(self):
        token = self.get_token('admin', 'admin')
        self.assertTrue(len(token)>0, 'test login failed')


if __name__ == "__main__":
    unittest.main()
