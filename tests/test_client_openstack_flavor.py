# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import time
import httplib2
from urllib import urlencode

from test_base import BaseTestCase


class OpenStackFlavorTestCase(BaseTestCase):
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


    def test_create_flavor_no_permission(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        data = {'name': '小型'}
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "flavors",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "403", 'test_create_flavor_no_permission failed')


    def test_create_flavor_no_enough_input(self):
        content = self.get_token('admin', 'admin')
        token = json.loads(content)['success']['token']
        data = {'name': '小型'}
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "flavors",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "400", 'test_create_flavor_no_enough_input failed')


    def test_create_flavor_duplicate_name(self):
        content = self.get_token('admin', 'admin')
        token = json.loads(content)['success']['token']
        data = {'name': 'm1.tiny', 'vcpus': 1, 'ram': 64, 'disk': 1, 'ephemeral': 0, 'swap': 0}
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "flavors",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "500", 'test_create_flavor_duplicate_name failed')


    def test_create_flavor(self):
        content = self.get_token('admin', 'admin')
        token = json.loads(content)['success']['token']
        data = {'name': '小型', 'vcpus': 1, 'ram': 64, 'disk': 1, 'ephemeral': 0, 'swap': 0}
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "flavors",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        flavor = json.loads(content)['flavor']
        self.assertTrue(flavor['id'], 'test_list_flavor failed')
        
        data = {'name': '小型1', 'vcpus': 11}
        resp, content = h.request(self.base_url + "flavors/" + "%s" % flavor['id'] ,
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )

        resp, content = h.request(self.base_url + "flavors/" + "%s" % flavor['id'],
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )


if __name__ == "__main__":
    unittest.main()
