# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import httplib2
from urllib import urlencode

from test_base import BaseTestCase
sys.path.append("..")
import appserver.model


class DeptTestCase(BaseTestCase):
    def test_error_token(self):
        h = httplib2.Http() 
        resp, content = h.request(self.base_url + "depts",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': "1234567890"}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "401", 'test error token failed')


    def test_list_dept(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http() 
        resp, content = h.request(self.base_url + "depts",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )  
        depts = json.loads(content)['depts']
        self.assertTrue(len(depts)>2, 'list_dept failed')


    def test_list_dept_no_permission(self):
        content = self.get_token('用户1', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()

        resp, content = h.request(self.base_url + "depts",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "403", 'list_dept_no_permission token failed')


    def test_show_dept_detail_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http() 
        resp, content = h.request(self.base_url + "depts/0",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )  
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_show_dept_detail_not_found failed')


    def test_show_dept_detail_no_permission(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http() 
        resp, content = h.request(self.base_url + "depts/1",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )  
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_show_dept_detail_no_permission failed')


    def test_show_dept_detail(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http() 
        resp, content = h.request(self.base_url + "depts/2",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )  
        dept = json.loads(content)['dept']
        self.assertEqual(dept['id'], 2, "test_show_dept_detail failed")


    def test_add_duplicate_dept(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http() 
        data = {'name': '研发部', 'desc': '研发部', 'parent_dept_id': 2}
        resp, content = h.request(self.base_url + "depts",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "400", 'test_add_duplicate_dept failed')


    def test_add_dept_parent_not_exist(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'name': '研发3部', 'desc': '研发3部', 'parent_dept_id': 100}
        resp, content = h.request(self.base_url + "depts",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_add_dept_parent_not_exist failed')

 
    def test_add_dept(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'name': '研发3部', 'desc': '研发3部', 'parent_dept_id': 2}
        resp, content = h.request(self.base_url + "depts",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        dept = json.loads(content)['dept']
        self.assertTrue(dept['id']>0, 'test_add_dept failed')

        resp, content = h.request(self.base_url + "depts/" + "%d" % dept['id'],
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )

    
    def test_delete_dept_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "depts/100",
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_delete_dept_not_found failed')


    def test_delete_dept_not_empty(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "depts/2",
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "400", 'test_delete_dept_not_empty failed')


    def test_delete_dept_no_permission(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "depts/1",
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "403", 'test_delete_dept_no_permission failed')


    def test_update_dept_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'name': '研发二部1', 'desc': '研发二部1', 'parent_dept_id': 2}
        resp, content = h.request(self.base_url + "depts/100",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_update_dept_not_found failed')


    def test_update_dept_no_permission(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'name': '研发二部1', 'desc': '研发二部1', 'parent_dept_id': 2}
        resp, content = h.request(self.base_url + "depts/1",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "403", 'test_update_dept_no_permission failed')


    def test_update_dept_no_parent(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'name': '研发二部1', 'desc': '研发二部1', 'parent_dept_id': 100}
        resp, content = h.request(self.base_url + "depts/3",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_update_dept_no_parent failed')


    def test_update_dept_name_exist(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'name': '研发二部', 'desc': '研发二部', 'parent_dept_id': 2}
        resp, content = h.request(self.base_url + "depts/3",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "400", 'test_update_dept_name_exist failed')


    def test_update_dept(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'name': '研发二部1', 'desc': '研发二部1', 'parent_dept_id': 2}
        resp, content = h.request(self.base_url + "depts/3",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )


if __name__ == "__main__":
    unittest.main()
