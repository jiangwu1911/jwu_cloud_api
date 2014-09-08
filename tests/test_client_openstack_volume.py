# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import time
import httplib2
from urllib import urlencode

from test_base import BaseTestCase


class OpenStackVolumeTestCase(BaseTestCase):
    def test_list_volume(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "volumes",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )


    def test_show_volume_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "volumes/100",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_show_volume_not_found failed')


    def test_delete_volume_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "volumes/100",
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_delete_volume_not_found failed')


    def atest_attach_operation_not_support(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'action': 'attach_volume', 'volume_id': 1}
        resp, content = h.request(self.base_url + "volumes/3",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        print content
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "400", 'test_attach_operation_not_support failed')


    def test_attach_server_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'action': 'attach', 'server_id': 100}
        resp, content = h.request(self.base_url + "volumes/3",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_attach_server_not_found failed')


    def test_attach_server_not_give(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'action': 'attach'}
        resp, content = h.request(self.base_url + "volumes/3",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "400", 'test_attach_server_not_give failed')


    def test_attach_volume_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'action': 'attach', 'server_id': 1}
        resp, content = h.request(self.base_url + "volumes/100",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_attach_volume_not_found failed')


    def test_attach_volume(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'action': 'attach', 'server_id': 1}
        resp, content = h.request(self.base_url + "volumes/3",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        print content


    def atest_create_volume(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'name': 'disk01', 'size': 1}
        resp, content = h.request(self.base_url + "volumes",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        print content
        volume = json.loads(content)['volume']
        self.assertTrue(volume['id']>0, 'test_list_flavor failed')

        time.sleep(10)
        resp, content = h.request(self.base_url + "volumes/%d" % volume['id'],
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        print content


if __name__ == "__main__":
    unittest.main()
