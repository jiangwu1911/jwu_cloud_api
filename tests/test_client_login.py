import sys
import unittest
import json
import httplib2
from urllib import urlencode

from test_base import BaseTestCase


class LoginTestCase(BaseTestCase):
    def test_login(self):
        token = self.get_token('admin', 'admin')
        print token


if __name__ == "__main__":
    unittest.main()
