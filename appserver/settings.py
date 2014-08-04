db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '',
    'db': 'cloudapi',
    'charset': 'utf8'
}

listen_ip = "0.0.0.0"
listen_port = 8080
token_expires = 86400

openstack_host = "192.168.206.128"
openstack_keystone_url = "http://%s:5000/v2.0" % openstack_host
openstack_keystone_default_role = "_member_"
openstack_user = "user01"
openstack_password = "abc1231"
openstack_tenant_name = "project01"
