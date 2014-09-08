# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import time
import httplib2
from urllib import urlencode

from test_base import BaseTestCase


class OpenStackSnapshotTestCase(BaseTestCase):
    def test_list_snapshot(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "snapshots",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )


    def test_show_snapshot_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "snapshots/100",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_show_snapshot_not_found failed')


    def test_show_snapshot(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "snapshots/3",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        snapshot = json.loads(content)['snapshot']
        self.assertTrue(snapshot['id']>0, 'test_show_snapshot failed')



    def test_delete_snapshot_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "snapshots/100",
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_delete_snapshot_not_found failed')


    def test_delete_snapshot(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "snapshots/3",
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        print content


if __name__ == "__main__":
    unittest.main()
