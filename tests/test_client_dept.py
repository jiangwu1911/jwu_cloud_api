# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import httplib2
from urllib import urlencode

from test_base import BaseTestCase
sys.path.append("..")
import appserver.model


class DeptTestCase(BaseTestCase):
    def test_list_dept(self):
        token = self.get_token('熊大', 'abc123')
        h = httplib2.Http() 

        resp, content = h.request(self.base_url + "dept",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )  
        print content


if __name__ == "__main__":
    unittest.main()
