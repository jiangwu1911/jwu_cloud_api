import logging
import threading
from kombu.mixins import ConsumerMixin
from kombu import Connection
from kombu import Exchange, Queue
from model import NovaNotification
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
