# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import time
import httplib2
from urllib import urlencode

from test_base import BaseTestCase


class MonitorTestCase(BaseTestCase):
    def test_get_data_no_permission(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "monitor/cpu",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "403", 'test_get_data_no_permission failed')


    def test_get_data_data_type_not_supported(self):
        content = self.get_token('admin', 'admin')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "monitor/temperature",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "400", 'test_get_data_data_type_not_supported failed')


    def test_get_data_without_host(self):
        content = self.get_token('admin', 'admin')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "monitor/cpu",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "400", 'test_get_data_without_host')


    def atest_get_data_cpu(self):
        content = self.get_token('admin', 'admin')
        token = json.loads(content)['success']['token']
        data = {'hostname': 'logclient'}
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "monitor/cpu",
                                  "GET",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        print content


    def test_get_data_memory(self):
        content = self.get_token('admin', 'admin')
        token = json.loads(content)['success']['token']
        data = {'hostname': 'logclient'}
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "monitor/memory",
                                  "GET",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )



if __name__ == "__main__":
    unittest.main()
