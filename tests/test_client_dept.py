# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import httplib2
from urllib import urlencode

import base
sys.path.append("..")
import appserver.model


class DeptTestCase(base.BaseTestCase):
    def test_list_dept(self):
        token = self.get_token('熊大', 'abc123')
        h = httplib2.Http() 

        resp, content = h.request(self.base_url + "dept",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )  
        data = json.loads(content)
        for d in data['depts']:
            print d['name']


if __name__ == "__main__":
    unittest.main()
