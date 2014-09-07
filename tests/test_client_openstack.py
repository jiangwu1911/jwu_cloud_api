# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import time
import httplib2
from urllib import urlencode

from test_base import BaseTestCase


class OpenStackTestCase(BaseTestCase):
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


    def test_create_server_flavor_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'image_name': 'image1', 'flavor_name': 'flavor1', 'server_name': 'vm102'}
        resp, content = h.request(self.base_url + "servers",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_create_server_flavor_not_found failed')


    def test_create_server_image_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'image_name': 'image1', 'flavor_name': 'm1.tiny', 'server_name': 'vm102'}
        resp, content = h.request(self.base_url + "servers",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_create_server_image_not_found failed')


    def test_create_server(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'image_name': 'TestVM', 'flavor_name': 'very_tiny', 'server_name': 'vm102'}
        resp, content = h.request(self.base_url + "servers",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        server = json.loads(content)['server']
        
        # Get server status
        resp, content = h.request(self.base_url + "servers/%d" % server['id'],
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        server = json.loads(content)['server']

        time.sleep(60)  # Wait for instance's state change to active
        
        # Suspend server
        data = {'action': 'suspend'}
        resp, content = h.request(self.base_url + "servers/%d" % server['id'],
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        
        # resume server
        time.sleep(10)  
        data = {'action': 'resume'}
        resp, content = h.request(self.base_url + "servers/%d" % server['id'],
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )

        time.sleep(10)  # Wait for instance's state change to active
        resp, content = h.request(self.base_url + "servers/%d" % server['id'],
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )

if __name__ == "__main__":
    unittest.main()
