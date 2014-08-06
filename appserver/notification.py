import logging
import threading
import datetime
from kombu.mixins import ConsumerMixin
from kombu import Connection
from kombu import Exchange, Queue
from model import NovaNotification
from model import Server
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import settings as conf

log = logging.getLogger("cloudapi")

class Worker(ConsumerMixin):
    def __init__(self, connection, db_engine):
        self.connection = connection
        self.db_engine = db_engine


class NovaWorker(Worker):
    def get_consumers(self, Consumer, channel):
        exchange = Exchange('nova', type='topic', durable=False, 
                            auto_delete=False, internal=False)
        queues = [Queue('cloudapi_nova', exchange, 
                        routing_key='notifications.info',
                        no_ack=True)]
        return [Consumer(queues=queues,
                         accept=['json'],
                         callbacks=[self.process_task])]


    def process_task(self, body, message):
        Session = sessionmaker(self.db_engine)
        session = Session()
    
        # Save notification in database
        payload = body.get('payload')
        notification = NovaNotification(
                        message_id = body.get('message_id', ''),
                        occurred_at = body.get('timestamp', ''),
                        event_type = body.get('event_type', ''),
                        instance_id = payload.get('instance_id', ''),
                        state = payload.get('state', ''),
                        old_state = payload.get('old_state', ''),
                        new_task_state = payload.get('new_task_state', ''),
                        old_task_state = payload.get('old_task_state', ''))
        session.add(notification)
        session.commit()

        server = session.query(Server).filter(Server.instance_id==notification.instance_id).first()
        if server:
            # Update server state
            server.state = notification.state
            server.task_state = notification.new_task_state
            server.updated_at = datetime.datetime.now()

            if notification.state=='deleted':
                server.deleted = 1
                server.deleted_at = datetime.datetime.now()

            session.add(server)
            session.commit()

            if notification.state=='active':
                # Get server's IP
                import novaclient.v1_1.client as nvclient
                nova_client = nvclient.Client(auth_url = conf.openstack_api['keystone_url'],
                                              username = conf.openstack_api['user'],
                                              api_key = conf.openstack_api['password'],
                                              project_id = conf.openstack_api['tenant_name']
                                             )
                instance = nova_client.servers.get(notification.instance_id).to_dict()
                ips = []
                for net in instance.get('addresses').values():
                    for n in net:
                        if n.get('addr'):
                            ips.append(n.get('addr'))
                server.ip = ','.join(ips)
                session.add(server)
                session.commit()

        session.close()

        
class NotifyListener(threading.Thread):
    def __init__(self, db_engine):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.db_engine = db_engine


class NovaNotifyListener(NotifyListener):
    def run(self):
        mq = conf.openstack_message_queue
        url = "amqp://%s:%s@%s:%d//" % (mq['nova_user'],
                                        mq['nova_password'],
                                        mq['host'],
                                        mq['port'])
        with Connection(url) as conn:
            try:
                worker = NovaWorker(conn, self.db_engine)
                worker.run()
            except KeyboardInterrupt:
                pass
