import sys
import unittest
import json
import httplib2
from urllib import urlencode


BASE_URL='http://localhost:8080/'
SERVER_PORT=80
TIMEOUT=30

class LoginTestCase(unittest.TestCase):
    def test_login(self):
        h = httplib2.Http() 
        data = {'username':'admin', 'password':'admin'}
        resp, content = h.request(BASE_URL + "login",
                                  "POST",
                                  urlencode(data), 
                                  headers={'Content-Type': 'application/x-www-form-urlencoded'})  
        print resp  
        print json.loads(content)


if __name__ == "__main__":
    unittest.main()
