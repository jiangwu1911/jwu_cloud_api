import sys
import unittest
import json
import httplib2
from urllib import urlencode
import base


class UserTestCase(base.BaseTestCase):
    def test_list_user(self):
        token = self.get_token()
        h = httplib2.Http() 
        resp, content = h.request(self.base_url + "user",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )  
        print json.loads(content)


if __name__ == "__main__":
    unittest.main()
