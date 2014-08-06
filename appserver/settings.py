db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '',
    'db': 'cloudapi',
    'charset': 'utf8',
}

listen_ip = "0.0.0.0"
listen_port = 8080
token_expires = 86400

openstack_api = {
    'keystone_url': 'http://192.168.206.100:5000/v2.0',
    'user': 'user01',
    'password': 'abc123',
    'tenant_name': 'project01',
}

openstack_message_queue = {
    'host': '192.168.206.100',
    'port': 5672,
    'nova_user': 'nova',
    'nova_password': 'segZWlwi',
}
