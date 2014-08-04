import sys
import unittest
import json
import httplib2
from urllib import urlencode

from test_base import BaseTestCase


class LoginTestCase(BaseTestCase):
    def test_login_wiith_wrong_username(self):
        content = self.get_token('admin1', 'admin')
        error = json.loads(content)['error']['code']
        self.assertEqual(error, "403", "test login with wrong username failed")


    def test_login_wiith_wrong_username(self):
        content = self.get_token('admin', 'admin1')
        error = json.loads(content)['error']['code']
        self.assertEqual(error, "403", "test login with wrong password failed")


    def test_login(self):
        content = self.get_token('admin', 'admin')
        token = json.loads(content)['success']['token']
        self.assertTrue(len(token)>0, 'test login failed')


if __name__ == "__main__":
    unittest.main()
