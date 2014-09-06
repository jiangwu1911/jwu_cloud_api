# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import time
import httplib2
from urllib import urlencode

from test_base import BaseTestCase


class OpenStackFlavorTestCase(BaseTestCase):
    def test_get_console(self):
        content = self.get_token('admin', 'admin')
        token = json.loads(content)['success']['token']
        data = {'action': 'get_console', 'console_type': 'novnc'}
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "servers/1",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        print content


if __name__ == "__main__":
    unittest.main()
