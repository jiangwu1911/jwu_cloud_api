# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import time
import httplib2
from urllib import urlencode

from test_base import BaseTestCase


class OpenStackHostTestCase(BaseTestCase):
    def test_list_hypervisor_no_permission(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "hosts",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "403", 'test_list_hypervisor_no_permission failed')


    def test_list_hypervisor(self):
        content = self.get_token('admin', 'admin')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "hosts",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        print content
        hypervisors = json.loads(content)['hypervisors']
        self.assertTrue(len(hypervisors)>=1, 'test_list_hypervisor failed')


    def test_stats_hypervisor(self):
        content = self.get_token('admin', 'admin')
        token = json.loads(content)['success']['token']
        data = {'action': 'stats'}
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "hosts",
                                  "GET",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        print content
        data = json.loads(content)['hypervisor_stats']
        self.assertTrue(len(data)>=1, 'test_list_hypervisor failed')


if __name__ == "__main__":
    unittest.main()
