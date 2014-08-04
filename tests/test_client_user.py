# -*- coding: UTF-8 -*-

import sys
import unittest
import json
import httplib2
from urllib import urlencode
from test_base import BaseTestCase
from appserver.utils import md5encode


class UserTestCase(BaseTestCase):
    def test_list_user(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "users",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )  
        users = json.loads(content)['users']
        self.assertTrue(len(users)>2, 'list_user failed')


    def test_list_user_with_deptid(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'dept_id': 4}
        resp, content = h.request(self.base_url + "users",
                                  "GET",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        users = json.loads(content)['users']
        self.assertTrue(len(users)>0, 'list_user_with_deptid failed')


    def test_show_user_not_found(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "users/100",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_show_user_not_found failed')


    def test_show_user_with_userid_not_permission(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "users/1",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_show_user_with_userid_not_permission failed')


    def test_show_user_with_userid(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "users/4",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        user = json.loads(content)['user']
        self.assertEqual(user['id'], 4, 'test_show_user_with_userid failed')


    def test_add_user_dup_username(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'username': '张三', 'password': md5encode('abc123'), 'dept_id': 3}
        resp, content = h.request(self.base_url + "users",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "400", 'test_show_user_dup_username failed')


    def test_add_user_dup_email(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'username': '张三1', 'email': 'zhangsan@test.com', 
                'password': md5encode('abc123'), 'dept_id': 3}
        resp, content = h.request(self.base_url + "users",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "400", 'test_add_user_dup_email failed')


    def test_add_user_not_dept_admin(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'username': '张三1', 'email': 'zhangsan1@test.com', 
                'password': md5encode('abc123'), 'dept_id': 1}
        resp, content = h.request(self.base_url + "users",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "403", 'test_add_user_not_dept_admin failed')


    def test_add_user_wrong_role_id(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'username': '张三1', 'email': 'zhangsan1@test.com', 
                'password': md5encode('abc123'), 'dept_id': 3, 'role_id': 1}
        resp, content = h.request(self.base_url + "users",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "403", 'test_add_user_wrong_role_id failed')


    def test_add_user(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'username': '张三1', 'email': 'zhangsan1@test.com', 
                'password': md5encode('abc123'), 'dept_id': 3}
        resp, content = h.request(self.base_url + "users",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        user = json.loads(content)['user']
        self.assertTrue(user['id']>0, 'test_add_user failed')

        resp, content = h.request(self.base_url + "users/" + "%d" % user['id'],
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )


    def test_delete_user_not_exist(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "users/100",
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_delete_user_not_exist failed')


    def test_delete_user_not_dept_admin(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        resp, content = h.request(self.base_url + "users/1",
                                  "DELETE",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "404", 'test_delete_user_not_dept_admin failed')


    def test_update_user_name_exist(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'username': '李四'}
        resp, content = h.request(self.base_url + "users/4",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "400", 'test_update_user_name_exist failed')


    def test_update_user_email_exist(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'email': 'lisi@test.com'}
        resp, content = h.request(self.base_url + "users/4",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "400", 'test_update_user_name_exist failed')


    def test_update_user_no_dept_permission(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'dept_id': 1}
        resp, content = h.request(self.base_url + "users/4",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "403", 'test_update_user_no_dept_permission failed')


    def test_update_user_no_role_permission(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'role_id': 1}
        resp, content = h.request(self.base_url + "users/4",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )
        error = json.loads(content)['error']
        self.assertEqual(error['code'], "403", 'test_update_user_no_role_permission failed')


    def test_update_user(self):
        content = self.get_token('熊大', 'abc123')
        token = json.loads(content)['success']['token']
        h = httplib2.Http()
        data = {'username': '李四1', 'password': md5encode('111111'), 'email': 'lisi1@test.com',
                'dept_id': 3, 'role_id': 3}
        resp, content = h.request(self.base_url + "users/11",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': token}
                                 )


if __name__ == "__main__":
    unittest.main()
