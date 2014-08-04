# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import httplib2
from urllib import urlencode

from test_base import BaseTestCase


class LoginTestCase(BaseTestCase):
    def test_list_flavor(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "flavors",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        flavors = json.loads(content)['flavors']
        self.assertTrue(len(flavors)>2, 'test_list_flavor failed')


    def test_list_image(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "images",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        images = json.loads(content)['images']
        self.assertTrue(len(images)>0, 'test_list_image failed')


    def test_list_server(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "servers",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        servers = json.loads(content)['servers']
        self.assertTrue(len(servers)>=0, 'test_list_server failed')


if __name__ == "__main__":
    unittest.main()
