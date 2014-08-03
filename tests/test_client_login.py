import sys
import unittest
import json
import httplib2
from urllib import urlencode

import base


class LoginTestCase(base.BaseTestCase):
    def test_login(self):
        token = self.get_token()
        print token


if __name__ == "__main__":
    unittest.main()
