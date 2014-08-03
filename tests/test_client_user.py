# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import httplib2
from urllib import urlencode
from test_base import BaseTestCase


class UserTestCase(BaseTestCase):
    def test_list_user(self):
        token = self.get_token('熊大', 'abc123')
        h = httplib2.Http() 
        resp, content = h.request(self.base_url + "user",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )  
        print json.loads(content)


if __name__ == "__main__":
    unittest.main()
