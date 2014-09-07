# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import time
import httplib2
from urllib import urlencode

from test_base import BaseTestCase


class OpenStackServerTestCase(BaseTestCase):
    def test_get_console(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        data = {'action': 'get_console', 'console_type': 'novnc'}
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "servers/2",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        url = json.loads(content)['console']['url']
        self.assertTrue(len(url)>0, 'test_get_console failed')


    def test_update_server_server_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        data = {'name': 'myserver'}
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "servers/1",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_update_server_server_not_found failed')


    def test_update_server_assign_to_wrong_user(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        data = {'owner': '1', 'name': 'myserver'}
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "servers/2",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_update_server_server_not_found failed')


    def test_update_server_assign_to_user(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        data = {'owner': '4', 'name': "zhangsan's server"}
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "servers/2",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )


if __name__ == "__main__":
    unittest.main()
