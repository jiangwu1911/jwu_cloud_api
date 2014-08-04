# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import httplib2
from urllib import urlencode
from test_base import BaseTestCase


class UserTestCase(BaseTestCase):
    def test_list_user(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "user",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )  
        users = json.loads(content)['users']
        self.assertTrue(len(users)>2, 'list_user failed')


    def test_list_user_with_deptid(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'dept_id': 4}
        resp, content = h.request(self.base_url + "user",
                                  "GET",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        users = json.loads(content)['users']
        self.assertTrue(len(users)>0, 'list_user_with_deptid failed')


if __name__ == "__main__":
    unittest.main()
