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
    def test_error_token(self):
        h = httplib2.Http() 
        resp, content = h.request(self.base_url + "dept",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': "1234567890"}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "401", 'test error token failed')


    def test_list_dept(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http() 
        resp, content = h.request(self.base_url + "dept",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )  
        depts = json.loads(content)['depts']
        self.assertEqual(len(depts), 3, 'list_dept failed')


    def test_list_dept_no_permission(self):
        content = self.get_token('用户1', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()

        resp, content = h.request(self.base_url + "dept",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "403", 'list_dept_no_permission token failed')


if __name__ == "__main__":
    unittest.main()
