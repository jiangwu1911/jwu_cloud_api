import sys
import unittest
import json
import httplib2
from urllib import urlencode

sys.path.append("..")
from appserver.utils import md5encode


class BaseTestCase(unittest.TestCase):
    base_url = 'http://localhost:8080/'

    def get_token(self, username, password):
        h = httplib2.Http() 
        data = {'username': username, 'password': md5encode(password)}
        resp, content = h.request(self.base_url + "login",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded'})
        
        return content 
