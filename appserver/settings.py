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
upload_files_path = '/tmp/jwu_cloud_api/'
static_files_path = '/home/python/jwu_cloud_app/'

openstack_api = {
    'keystone_url': 'http://192.168.145.11:5000/v2.0',
    'user': 'user01',
    'password': 'abc123',
    'tenant_name': 'project01',

    'admin_user': 'admin',
    'admin_password': 'admin',
    'admin_tenant_name': 'admin',
}

openstack_message_queue = {
    'host': '192.168.145.11',
    'port': 5672,
    'nova_user': 'nova',
    'nova_password': 'PyPKep6v',
}
